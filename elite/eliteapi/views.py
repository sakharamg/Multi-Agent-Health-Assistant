from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import transformers
from peft import PeftModel, PeftConfig
from twilio.rest import Client
import json
import torch
import re
import ast

from .functional_apis import retrieve_past_complaints, get_available_specialists, confirm_appointment
from monitor.reminders import ReminderManager

from .utils import SmartwatchSimulator
from .models import PatientVitals, Reminders

planner_model  = None
planner_tokenizer = None

caller_model = None
caller_tokenizer = None

def postprocess(text):
    """
    Process the input text to remove certain patterns and ensure it starts and ends in JSON format.
    
    Parameters:
    text (str): The input text to be processed.
    
    Returns:
    str: The processed text after removing specified patterns and ensuring proper starting characters.
    """
    pattern = r'reason'
    match = re.search(pattern, text)
    if match:
        text = text[match.start():]
    if "{'" not in text[:4] or '{"' not in text[:4]:
        if '"' in text[:8]:
            text = '{"'+text.strip()
        else:
            text = "{'"+text.strip()
    pattern = r'</s>'
    match = re.search(pattern, text)
    if match:
        text = text[:match.start()]
    pattern = r'Action: '
    match = re.search(pattern, text)
    if match:
        text = text[:match.start()]
    return text

def postprocess_caller(text):
    """
    Process the input text to remove certain patterns and ensure it starts and ends in JSON format.
    
    Parameters:
    text (str): The input text to be processed.
    
    Returns:
    str: The processed text after removing specified patterns and ensuring proper starting characters.
    """
    if "{'" not in text[:4] or '{"' not in text[:4]:
        if '"' in text[:8]:
            text = '{"'+text.strip()
        else:
            text = "{'"+text.strip()
    pattern = r'Next: <[^>]*>'
    match = re.search(pattern, text)
    if match:
        text =  text[:match.start()]
    pattern = r'</s>'
    match = re.search(pattern, text)
    if match:
        text = text[:match.start()]
    return text

def generate_plan(query):
    input = """You have access to the following apis:\n{\'Name\': \'get_available_specialists\', \'Description\': \'Fetches a list of specialists and their availability.\', \'Parameters\': [{\'param_name\': \'symptoms\', \'type\': \'string\', \'default\': \'None\', \'description\': \'List of symptoms derived from user input.\'}, {\'param_name\': \'specialization\', \'type\': \'string\', \'default\': \'None\', \'description\': \'specialization name for the appointment\'}, {\'param_name\': \'user_schedule\', \'type\': \'object\', \'default\': \'None\', \'description\': "User\'s preferred schedule for appointments in key-value pairs (e.g., {\'date\': \'YYYY-MM-DD\', \'time_range\': \'HH:MM-HH:MM\'})."}], \'Required Parameters\': [\'symptoms\', \'specialization\'], \'Returns\': {\'type\': \'dictionary\', \'description\': \' returns single best schedule {specialist_id,name, available_slot including time in HH:MM-HH:MM format and date in DD/MM/YY format}.\'}}, {\'Name\': \'confirm_appointment\', \'Description\': "Confirms an appointment slot and stores it in the hospital\'s database.", \'Parameters\': [{\'param_name\': \'user_id\', \'type\': \'string\', \'default\': \'None\', \'description\': \'Unique identifier for the user.\'}, {\'param_name\': \'specialist_id\', \'type\': \'string\', \'default\': \'None\', \'description\': \'Unique identifier for the chosen specialist.\'}, {\'param_name\': \'appointment_time_date\', \'type\': \'string\', \'default\': \'None\', \'description\': \'The selected time slot for the appointment as time in HH:MM-HH:MM format and date in DD/MM/YY format.\'}], \'Required Parameters\': [\'user_id\', \'specialist_id\', \'appointment_time\'], \'Returns\': {\'type\': \'boolean\', \'description\': \'Always returns True.\'}}, {\'Name\': \'save_appointment_history\', \'Description\': "Saves appointment information in the user\'s database for later reference and recurring use cases.", \'Parameters\': [{\'param_name\': \'user_id\', \'type\': \'string\', \'default\': \'None\', \'description\': \'Unique identifier for the user.\'}, {\'param_name\': \'symptoms\', \'type\': \'string\', \'default\': \'None\', \'description\': \'The symptoms described by the user.\'}, {\'param_name\': \'specialist_id\', \'type\': \'string\', \'default\': \'None\', \'description\': \'Unique identifier for the chosen specialist.\'}, {\'param_name\': \'appointment_time_date\', \'type\': \'string\', \'default\': \'None\', \'description\': \'The selected time slot for the appointment as time in HH:MM-HH:MM format and date in DD/MM/YY format.\'}], \'Required Parameters\': [\'user_id\', \'symptoms\', \'specialist_id\', \'appointment_time_date\'], \'Returns\': {\'type\': \'boolean\', \'description\': \'Always true\'}}, {\'Name\': \'get_appointment_history\', \'Description\': "Retrieves the user\'s appointment history for analysis and reminders.", \'Parameters\': [{\'param_name\': \'user_id\', \'type\': \'string\', \'default\': \'None\', \'description\': \'Unique identifier for the user.\'}], \'Required Parameters\': [\'user_id\'], \'Returns\': {\'type\': \'array\', \'description\': \'Array containing past appointment records.\'}}, {\'Name\': \'retrieve_past_complaints\', \'Description\': "Fetches the user\'s past complaints matching the given symptoms for analysis and reference.", \'Parameters\': [{\'param_name\': \'user_id\', \'type\': \'string\', \'default\': \'None\', \'description\': \'Unique identifier for the user.\'}, {\'param_name\': \'symptoms\', \'type\': \'string\', \'default\': \'None\', \'description\': \'List of symptoms to search for in past complaints.\'}, {\'param_name\': \'date_range\', \'type\': \'object\', \'default\': \'None\', \'description\': "Optional date range filter in the format {\'start_date\': \'YYYY-MM-DD\', \'end_date\': \'YYYY-MM-DD\'}."}], \'Required Parameters\': [\'user_id\', \'symptoms\'], \'Returns\': {\'type\': \'array\', \'description\': \'Array of past complaints related to the specified symptoms.\'}}, {\'Name\': \'follow_up_with_user\', \'Description\': \'Initiates a follow-up interaction with the user based on their past complaints and current symptoms.\', \'Parameters\': [{\'param_name\': \'user_id\', \'type\': \'string\', \'default\': \'None\', \'description\': \'Unique identifier for the user.\'}, {\'param_name\': \'past_complaints\', \'type\': \'array\', \'default\': \'[]\', \'description\': \'List of past complaints to reference during the follow-up.\'}, {\'param_name\': \'current_symptoms\', \'type\': \'string\', \'default\': \'None\', \'description\': \'Current symptoms reported by the user.\'}, {\'param_name\': \'preferred_contact_method\', \'type\': \'string\', \'default\': \'None\', \'description\': "User\'s preferred method for follow-up (e.g., \'call\', \'email\', \'chat\')."}], \'Required Parameters\': [\'user_id\', \'current_symptoms\'], \'Returns\': {\'type\': \'object\', \'description\': \'Details of the follow-up initiated, including method and next steps.\'}}, {\'Name\': \'notify_user\', \'Description\': \'Sends a notification to the user \', \'Parameters\': [{\'param_name\': \'user_id\', \'type\': \'string\', \'default\': \'None\', \'description\': \'Unique identifier for the user.\'}, {\'param_name\': \'message\', \'type\': \'string\', \'default\': \'None\', \'description\': \'The notification message to send.\'}], \'Required Parameters\': [\'user_id\', \'message\'], \'Returns\': {\'type\': \'boolean\', \'description\': \'Always returns status as True\'}}, {\'Name\': \'get_input_from_user\', \'Description\': \'Collects input from the user for specified parameters.\', \'Parameters\': [{\'param_name\': \'user_id\', \'type\': \'string\', \'default\': \'None\', \'description\': \'Unique identifier for the user.\'}, {\'param_name\': \'questions\', \'type\': \'string\', \'default\': \'[]\', \'description\': \'Question to ask the user.\'}], \'Required Parameters\': [\'user_id\', \'questions\'], \'Returns\': {\'type\': \'string\', \'description\': "User\'s response to the specified questions."}}, {\'Name\': \'store_symptoms\', \'Description\': \'Stores the symptoms reported by the user and initiates a follow-up process to gather additional details for a more accurate analysis.\', \'Parameters\': [{\'param_name\': \'user_id\', \'type\': \'string\', \'default\': \'None\', \'description\': \'Unique identifier for the user.\'}, {\'param_name\': \'symptoms\', \'type\': \'string\', \'default\': \'None\', \'description\': \'Symptoms of user.\'}, {\'param_name\': \'timestamp\', \'type\': \'object\', \'default\': \'None\', \'description\': \'Save date and time of the event\', \'Required Parameters\': [\'user_id\', \'symptoms\', \'timestamp\'], \'Returns\': {\'type\': \'boolean\', \'description\': \'Status always true\'}}]}\n\nThe conversation history is: \n"""+query+"</s> Planner:"
    global planner_tokenizer
    # with open("/home/jagdish/storage/Multi-LLM-Agent/GLPFT/dataset/lite/train_test/planner_data_v1.5.json", 'r') as file:
    #     data = json.load(file)
    print("Input: ", input)
    # Print the data
    # print(data)
    # input = data[2]['input']
    model_inputs = planner_tokenizer([input], return_tensors="pt").to("cuda:1")
    generated_ids = planner_model.generate(
        **model_inputs,
        max_new_tokens=512,
        # temperature=0.01
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = planner_tokenizer.batch_decode(generated_ids)[0]
    return response

def generate_caller_response(query):
    """
    Generates a plan using LLM, based on the given query using a pre-defined set of APIs and conversation history.

    Parameters:
    query (str): The input query that contains the conversation history.

    Returns:
    str: The generated plan based on the input query.
    """
    # input = "You have access to the following apis:\n{'Name': 'get_available_specialists', 'Description': 'Fetches a list of specialists and their availability.', 'Parameters': [{'param_name': 'symptoms', 'type': 'string', 'default': 'None', 'description': 'List of symptoms derived from user input.'}, {'param_name': 'specialization', 'type': 'string', 'default': 'None', 'description': 'specialization name for the appointment'}, {'param_name': 'user_schedule', 'type': 'object', 'default': 'None', 'description': \"User's preferred schedule for appointments in key-value pairs (e.g., {'date': 'YYYY-MM-DD', 'time_range': 'HH:MM-HH:MM'}).\"}], 'Required Parameters': ['symptoms', 'specialization'], 'Returns': {'type': 'dictionary', 'description': ' returns single best schedule {specialist_id,name, available_slot including time in HH:MM-HH:MM format and date in DD/MM/YY format}.'}}, {'Name': 'confirm_appointment', 'Description': \"Confirms an appointment slot and stores it in the hospital's database.\", 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'specialist_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the chosen specialist.'}, {'param_name': 'appointment_time_date', 'type': 'string', 'default': 'None', 'description': 'The selected time slot for the appointment as time in HH:MM-HH:MM format and date in DD/MM/YY format.'}], 'Required Parameters': ['user_id', 'specialist_id', 'appointment_time'], 'Returns': {'type': 'boolean', 'description': 'Always returns True.'}}, {'Name': 'save_appointment_history', 'Description': \"Saves appointment information in the user's database for later reference and recurring use cases.\", 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'symptoms', 'type': 'string', 'default': 'None', 'description': 'The symptoms described by the user.'}, {'param_name': 'specialist_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the chosen specialist.'}, {'param_name': 'appointment_time_date', 'type': 'string', 'default': 'None', 'description': 'The selected time slot for the appointment as time in HH:MM-HH:MM format and date in DD/MM/YY format.'}], 'Required Parameters': ['user_id', 'symptoms', 'specialist_id', 'appointment_time_date'], 'Returns': {'type': 'boolean', 'description': 'Always true'}}, {'Name': 'get_appointment_history', 'Description': \"Retrieves the user's appointment history for analysis and reminders.\", 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}], 'Required Parameters': ['user_id'], 'Returns': {'type': 'array', 'description': 'Array containing past appointment records.'}}, {'Name': 'retrieve_past_complaints', 'Description': \"Fetches the user's past complaints matching the given symptoms for analysis and reference.\", 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'symptoms', 'type': 'string', 'default': 'None', 'description': 'List of symptoms to search for in past complaints.'}, {'param_name': 'date_range', 'type': 'object', 'default': 'None', 'description': \"Optional date range filter in the format {'start_date': 'YYYY-MM-DD', 'end_date': 'YYYY-MM-DD'}.\"}], 'Required Parameters': ['user_id', 'symptoms'], 'Returns': {'type': 'array', 'description': 'Array of past complaints related to the specified symptoms.'}}, {'Name': 'follow_up_with_user', 'Description': 'Initiates a follow-up interaction with the user based on their past complaints and current symptoms.', 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'past_complaints', 'type': 'array', 'default': '[]', 'description': 'List of past complaints to reference during the follow-up.'}, {'param_name': 'current_symptoms', 'type': 'string', 'default': 'None', 'description': 'Current symptoms reported by the user.'}, {'param_name': 'preferred_contact_method', 'type': 'string', 'default': 'None', 'description': \"User's preferred method for follow-up (e.g., 'call', 'email', 'chat').\"}], 'Required Parameters': ['user_id', 'current_symptoms'], 'Returns': {'type': 'object', 'description': 'Details of the follow-up initiated, including method and next steps.'}}, {'Name': 'notify_user', 'Description': 'Sends a notification to the user ', 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'message', 'type': 'string', 'default': 'None', 'description': 'The notification message to send.'}], 'Required Parameters': ['user_id', 'message'], 'Returns': {'type': 'boolean', 'description': 'Always returns status as True'}}, {'Name': 'get_input_from_user', 'Description': 'Collects input from the user for specified parameters.', 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'questions', 'type': 'string', 'default': '[]', 'description': 'Question to ask the user.'}], 'Required Parameters': ['user_id', 'questions'], 'Returns': {'type': 'string', 'description': \"User's response to the specified questions.\"}}, {'Name': 'store_symptoms', 'Description': 'Stores the symptoms reported by the user and initiates a follow-up process to gather additional details for a more accurate analysis.', 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'symptoms', 'type': 'string', 'default': 'None', 'description': 'Symptoms of user.'}, {'param_name': 'timestamp', 'type': 'object', 'default': 'None', 'description': 'Save date and time of the event', 'Required Parameters': ['user_id', 'symptoms', 'timestamp'], 'Returns': {'type': 'boolean', 'description': 'Status always true'}}]}\n\nThe conversation history is:\nUser: I've been feeling very anxious and irritable lately.</s>Planner: {'reason': 'User reports symptoms of anxiety and irritability, but I need to clarify if there are any physical symptoms or triggers.', 'action': 'Ask user if they have experienced any physical symptoms or specific triggers for their anxiety.'}</s>Action: "
    input = "You have access to the following apis:\n{'Name': 'get_available_specialists', 'Description': 'Fetches a list of specialists and their availability.', 'Parameters': [{'param_name': 'symptoms', 'type': 'string', 'default': 'None', 'description': 'List of symptoms derived from user input.'}, {'param_name': 'specialization', 'type': 'string', 'default': 'None', 'description': 'specialization name for the appointment'}, {'param_name': 'user_schedule', 'type': 'object', 'default': 'None', 'description': \"User's preferred schedule for appointments in key-value pairs (e.g., {'date': 'YYYY-MM-DD', 'time_range': 'HH:MM-HH:MM'}).\"}], 'Required Parameters': ['symptoms', 'specialization'], 'Returns': {'type': 'dictionary', 'description': ' returns single best schedule {specialist_id,name, available_slot including time in HH:MM-HH:MM format and date in DD/MM/YY format}.'}}, {'Name': 'confirm_appointment', 'Description': \"Confirms an appointment slot and stores it in the hospital's database.\", 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'specialist_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the chosen specialist.'}, {'param_name': 'appointment_time_date', 'type': 'string', 'default': 'None', 'description': 'The selected time slot for the appointment as time in HH:MM-HH:MM format and date in DD/MM/YY format.'}], 'Required Parameters': ['user_id', 'specialist_id', 'appointment_time'], 'Returns': {'type': 'boolean', 'description': 'Always returns True.'}}, {'Name': 'save_appointment_history', 'Description': \"Saves appointment information in the user's database for later reference and recurring use cases.\", 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'symptoms', 'type': 'string', 'default': 'None', 'description': 'The symptoms described by the user.'}, {'param_name': 'specialist_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the chosen specialist.'}, {'param_name': 'appointment_time_date', 'type': 'string', 'default': 'None', 'description': 'The selected time slot for the appointment as time in HH:MM-HH:MM format and date in DD/MM/YY format.'}], 'Required Parameters': ['user_id', 'symptoms', 'specialist_id', 'appointment_time_date'], 'Returns': {'type': 'boolean', 'description': 'Always true'}}, {'Name': 'get_appointment_history', 'Description': \"Retrieves the user's appointment history for analysis and reminders.\", 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}], 'Required Parameters': ['user_id'], 'Returns': {'type': 'array', 'description': 'Array containing past appointment records.'}}, {'Name': 'retrieve_past_complaints', 'Description': \"Fetches the user's past complaints matching the given symptoms for analysis and reference.\", 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'symptoms', 'type': 'string', 'default': 'None', 'description': 'List of symptoms to search for in past complaints.'}, {'param_name': 'date_range', 'type': 'object', 'default': 'None', 'description': \"Optional date range filter in the format {'start_date': 'YYYY-MM-DD', 'end_date': 'YYYY-MM-DD'}.\"}], 'Required Parameters': ['user_id', 'symptoms'], 'Returns': {'type': 'array', 'description': 'Array of past complaints related to the specified symptoms.'}}, {'Name': 'follow_up_with_user', 'Description': 'Initiates a follow-up interaction with the user based on their past complaints and current symptoms.', 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'past_complaints', 'type': 'array', 'default': '[]', 'description': 'List of past complaints to reference during the follow-up.'}, {'param_name': 'current_symptoms', 'type': 'string', 'default': 'None', 'description': 'Current symptoms reported by the user.'}, {'param_name': 'preferred_contact_method', 'type': 'string', 'default': 'None', 'description': \"User's preferred method for follow-up (e.g., 'call', 'email', 'chat').\"}], 'Required Parameters': ['user_id', 'current_symptoms'], 'Returns': {'type': 'object', 'description': 'Details of the follow-up initiated, including method and next steps.'}}, {'Name': 'notify_user', 'Description': 'Sends a notification to the user ', 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'message', 'type': 'string', 'default': 'None', 'description': 'The notification message to send.'}], 'Required Parameters': ['user_id', 'message'], 'Returns': {'type': 'boolean', 'description': 'Always returns status as True'}}, {'Name': 'get_input_from_user', 'Description': 'Collects input from the user for specified parameters.', 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'questions', 'type': 'string', 'default': '[]', 'description': 'Question to ask the user.'}], 'Required Parameters': ['user_id', 'questions'], 'Returns': {'type': 'string', 'description': \"User's response to the specified questions.\"}}, {'Name': 'store_symptoms', 'Description': 'Stores the symptoms reported by the user and initiates a follow-up process to gather additional details for a more accurate analysis.', 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'symptoms', 'type': 'string', 'default': 'None', 'description': 'Symptoms of user.'}, {'param_name': 'timestamp', 'type': 'object', 'default': 'None', 'description': 'Save date and time of the event', 'Required Parameters': ['user_id', 'symptoms', 'timestamp'], 'Returns': {'type': 'boolean', 'description': 'Status always true'}}]}\n\nThe conversation history is:\n"+query
    global caller_tokenizer
    print("Input: ", input)
    model_inputs = caller_tokenizer([input], return_tensors="pt").to("cuda:0")
    generated_ids = caller_model.generate(
        **model_inputs,
        max_new_tokens=100,
        # temperature=0.01
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = caller_tokenizer.batch_decode(generated_ids)[0]
    return response

def load_planner_model():
    """
    Load the planner model and tokenizer from the specified path.
    
    This function initializes the planner model and tokenizer using the specified path.
    """
    global planner_model
    global planner_tokenizer
    print("[Planner]: Initializing planner model")
    PATH="/home/jagdish/storage/Multi-LLM-Agent/GLPFT/saved_models/toolbench/Qwen2.5-Coder-7B-Instruct/planner_v2-one-third"
    config = PeftConfig.from_pretrained(PATH)
    planner_tokenizer = transformers.AutoTokenizer.from_pretrained(
            config.base_model_name_or_path,
            use_fast=False,
    )

    
    planner_model = transformers.AutoModelForCausalLM.from_pretrained(
        config.base_model_name_or_path,
        device_map="cuda:1"
    )
    planner_model = PeftModel.from_pretrained(planner_model, PATH)
    # planner_model= planner_model.merge_and_unload()
    # print(planner_model)

def load_caller_model():
    """
    Load the caller model and tokenizer from the specified path.
    
    This function initializes the caller model and tokenizer using the specified path.
    """
    global caller_model
    global caller_tokenizer
    print("[Caller]: Initializing caller model")
    PATH="/home/jagdish/storage/Multi-LLM-Agent/GLPFT/saved_models/caller_v1.5"
    config = PeftConfig.from_pretrained(PATH)
    caller_tokenizer = transformers.AutoTokenizer.from_pretrained(
            config.base_model_name_or_path,
            use_fast=False,
    )

    
    caller_model = transformers.AutoModelForCausalLM.from_pretrained(
        config.base_model_name_or_path,
        device_map="cuda:0"
    )
    caller_model = PeftModel.from_pretrained(caller_model, PATH)
    caller_model= caller_model.merge_and_unload()
    # print(caller_model)

load_planner_model()
load_caller_model()

# Create your views here.
def printHelloWorld(request):
    return HttpResponse("Hello world")


def modelResponse(request):
    # load the logic
    return JsonResponse({
        "model": "xLam 3.5B",
        "text": "To plan a trip from the current place to Bangalore from 15th to 21st december, I need to gather information about the current situation, flights available, and hotel accomodation available."
    }, safe=False)

@csrf_exempt
def plannerResponse(request):
    """
    Handle the planner response endpoint.
    
    This function handles the POST request made to the planner response endpoint.
    It extracts the JSON query from the request body, generates a plan based on the query,
    processes the response, converts it to a JSON response, and returns it.
    
    Parameters:
    request (HttpRequest): The incoming HTTP request containing the query.
    
    Returns:
    JsonResponse: The JSON response containing the processed plan.
    """
    json_query = json.loads(request.body)
    query = json_query['query']
    response = generate_plan(query)
    print(response)
    json_resp = ast.literal_eval(postprocess(response))
    return JsonResponse(json_resp)

@csrf_exempt
def plannerTestResponse(request):
    # json_query = json.loads(request.body)
    # query = json_query['query']
    query="You have access to the following apis:\n{'Name': 'get_available_specialists', 'Description': 'Fetches a list of specialists and their availability.', 'Parameters': [{'param_name': 'symptoms', 'type': 'string', 'default': 'None', 'description': 'List of symptoms derived from user input.'}, {'param_name': 'specialization', 'type': 'string', 'default': 'None', 'description': 'specialization name for the appointment'}, {'param_name': 'user_schedule', 'type': 'object', 'default': 'None', 'description': \"User's preferred schedule for appointments in key-value pairs (e.g., {'date': 'YYYY-MM-DD', 'time_range': 'HH:MM-HH:MM'}).\"}], 'Required Parameters': ['symptoms', 'specialization'], 'Returns': {'type': 'dictionary', 'description': ' returns single best schedule {specialist_id,name, available_slot including time in HH:MM-HH:MM format and date in DD/MM/YY format}.'}}, {'Name': 'confirm_appointment', 'Description': \"Confirms an appointment slot and stores it in the hospital's database.\", 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'specialist_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the chosen specialist.'}, {'param_name': 'appointment_time_date', 'type': 'string', 'default': 'None', 'description': 'The selected time slot for the appointment as time in HH:MM-HH:MM format and date in DD/MM/YY format.'}], 'Required Parameters': ['user_id', 'specialist_id', 'appointment_time'], 'Returns': {'type': 'boolean', 'description': 'Always returns True.'}}, {'Name': 'save_appointment_history', 'Description': \"Saves appointment information in the user's database for later reference and recurring use cases.\", 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'symptoms', 'type': 'string', 'default': 'None', 'description': 'The symptoms described by the user.'}, {'param_name': 'specialist_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the chosen specialist.'}, {'param_name': 'appointment_time_date', 'type': 'string', 'default': 'None', 'description': 'The selected time slot for the appointment as time in HH:MM-HH:MM format and date in DD/MM/YY format.'}], 'Required Parameters': ['user_id', 'symptoms', 'specialist_id', 'appointment_time_date'], 'Returns': {'type': 'boolean', 'description': 'Always true'}}, {'Name': 'get_appointment_history', 'Description': \"Retrieves the user's appointment history for analysis and reminders.\", 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}], 'Required Parameters': ['user_id'], 'Returns': {'type': 'array', 'description': 'Array containing past appointment records.'}}, {'Name': 'retrieve_past_complaints', 'Description': \"Fetches the user's past complaints matching the given symptoms for analysis and reference.\", 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'symptoms', 'type': 'string', 'default': 'None', 'description': 'List of symptoms to search for in past complaints.'}, {'param_name': 'date_range', 'type': 'object', 'default': 'None', 'description': \"Optional date range filter in the format {'start_date': 'YYYY-MM-DD', 'end_date': 'YYYY-MM-DD'}.\"}], 'Required Parameters': ['user_id', 'symptoms'], 'Returns': {'type': 'array', 'description': 'Array of past complaints related to the specified symptoms.'}}, {'Name': 'follow_up_with_user', 'Description': 'Initiates a follow-up interaction with the user based on their past complaints and current symptoms.', 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'past_complaints', 'type': 'array', 'default': '[]', 'description': 'List of past complaints to reference during the follow-up.'}, {'param_name': 'current_symptoms', 'type': 'string', 'default': 'None', 'description': 'Current symptoms reported by the user.'}, {'param_name': 'preferred_contact_method', 'type': 'string', 'default': 'None', 'description': \"User's preferred method for follow-up (e.g., 'call', 'email', 'chat').\"}], 'Required Parameters': ['user_id', 'current_symptoms'], 'Returns': {'type': 'object', 'description': 'Details of the follow-up initiated, including method and next steps.'}}, {'Name': 'notify_user', 'Description': 'Sends a notification to the user ', 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'message', 'type': 'string', 'default': 'None', 'description': 'The notification message to send.'}], 'Required Parameters': ['user_id', 'message'], 'Returns': {'type': 'boolean', 'description': 'Always returns status as True'}}, {'Name': 'get_input_from_user', 'Description': 'Collects input from the user for specified parameters.', 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'questions', 'type': 'string', 'default': '[]', 'description': 'Question to ask the user.'}], 'Required Parameters': ['user_id', 'questions'], 'Returns': {'type': 'string', 'description': \"User's response to the specified questions.\"}}, {'Name': 'store_symptoms', 'Description': 'Stores the symptoms reported by the user and initiates a follow-up process to gather additional details for a more accurate analysis.', 'Parameters': [{'param_name': 'user_id', 'type': 'string', 'default': 'None', 'description': 'Unique identifier for the user.'}, {'param_name': 'symptoms', 'type': 'string', 'default': 'None', 'description': 'Symptoms of user.'}, {'param_name': 'timestamp', 'type': 'object', 'default': 'None', 'description': 'Save date and time of the event', 'Required Parameters': ['user_id', 'symptoms', 'timestamp'], 'Returns': {'type': 'boolean', 'description': 'Status always true'}}]}\n\nThe conversation history is:\nUser: I've been feeling very anxious and irritable lately.</s>Planner: {'reason': 'User reports symptoms of anxiety and irritability, but I need to clarify if there are any physical symptoms or triggers.', 'action': 'Ask user if they have experienced any physical symptoms or specific triggers for their anxiety.'}</s>Action: {'tool': 'get_input_from_user', 'parameters': {'user_id': '789', 'questions': 'Have you experienced any physical symptoms or specific triggers for your anxiety?'}}Observation: {'result': {'user': \"I've had trouble sleeping and I've been feeling restless.\"}}Planner: "
    response = generate_plan(query)
    print(response)
    response = postprocess(response)
    # json_resp = ast.literal_eval(postprocess(response))
    return HttpResponse(response)

@csrf_exempt
def callerResponse(request):
    """
    This function handles the HTTP request for generating a response based on the user's query. 
    It processes the input JSON data, generates a response using the `generate_caller_response` function, 
    and then formats the response using the `postprocess_caller` function. The function also handles specific API calls such as retrieving past complaints, 
    fetching available specialists, and confirming appointments by appending observations to the response. 
    Finally, it returns the processed response as a JSON object.

    Attributes:
        request (HTTPRequest): The incoming HTTP request containing the user's query.

    Returns:
        JsonResponse: A JSON response object containing the generated response and any relevant observations.
    """
    json_query = json.loads(request.body)
    print('BODY: ',json_query)
    query = json_query['query']
    response = generate_caller_response(query)
    json_resp = postprocess_caller(response)
    print(response)
    json_resp = ast.literal_eval(json_resp)
    if 'retrieve_past_complaints' in response:
        json_resp['history'] = json.dumps(json_resp)+"Observation: {'result': '" + retrieve_past_complaints(query[-50:]) + "'}}"
    if 'get_available_specialists' in response:
        json_resp['history'] = json.dumps(json_resp)+"Observation: {'result': '" + get_available_specialists(query[-50:]) + "'}}"
    if 'confirm_appointment' in response:
        json_resp['history'] = json.dumps(json_resp)+"Observation: {'result': '" + confirm_appointment() + "'}}"
    return JsonResponse(json_resp, safe=False)


def getSmartWatchStats(request):
    """
    Retrieves health statistics from a simulated smartwatch and returns them as a JSON response.

    Parameters:
    request (HttpRequest): The HTTP request object containing any necessary data or context for the request.

    Returns:
    JsonResponse: A JSON response containing the health data retrieved from the smartwatch simulator.
    """
    smartwatch = SmartwatchSimulator()
    health_data = smartwatch.get_vitals()
    return JsonResponse(health_data, safe=False)

def detectAbnormality(request):
    patientObj = PatientVitals.objects.latest('timestamp')
    return JsonResponse(patientObj.__dict__['vitals'], safe=False)

@csrf_exempt
def createReminders(request):
    """
    Creates reminders based on the provided query and returns them as a JSON response.

    Parameters:
    request (HttpRequest): The HTTP request object containing the body with the query data.

    Returns:
    JsonResponse: A JSON response containing the created reminders.
    """
    data = json.loads(request.body)
    json_query = data['query']
    reminder_manager = ReminderManager(json.dumps(json_query), planner_model)
    reminders = reminder_manager.run()
    return JsonResponse(reminders, safe=False)
    
def getReminders(request):  
    """
    Retrieves all reminders from the database and returns them as a JSON response.

    Parameters:
    request (HttpRequest): The HTTP request object containing any necessary data or context for the request.

    Returns:
    JsonResponse: A JSON response containing a list of dictionaries with details of each reminder.
    """
    reminders = Reminders.objects.all()
    result = []
    for reminder in reminders:
        data = {}
        data['title'] = reminder.title
        data['description'] = reminder.description
        data['time'] = reminder.time
        data['remaining_days'] = reminder.remaining_days
        result.append(data)
    return JsonResponse(result, safe=False)

@csrf_exempt
def sendReminders(request):
    """
    Sends a reminder message via SMS using Twilio API.

    Parameters:
    request (HttpRequest): The HTTP request object containing the reminder message in the request body.

    Returns:
    JsonResponse: A JSON response indicating the status of the reminder message sending process.
    """
    json_data = json.loads(request.body)
    reminder_body = json_data['reminder']
    print(reminder_body)
    # return JsonResponse({"body": reminder_body}, safe=False)
    account_sid = '<your account sid>'
    auth_token = '<your client id>'
    client = Client(account_sid, auth_token)

    # # Create Twilio client
    # client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=reminder_body,
            from_="+<twilio number>",
            to="+<receiver number>"
        )
        return JsonResponse({"status":"success"}, safe=False)
    except:
        return JsonResponse({"status": "error"})


