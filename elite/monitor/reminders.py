import json
from datetime import datetime, timedelta
import transformers
from peft import PeftConfig, PeftModel
import json
import torch

import threading
import time
from datetime import datetime, timedelta
from eliteapi.models import Reminders, Patient
planner_model = None
planner_tokenizer = None

def load_planner_model():
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

# from plyer import notification

class ReminderManager:
    """
    A class to manage reminders from prescriptions using an LLM for processing.
    """

    def __init__(self, prescription, llm):
        
        self.prescription = prescription
        # self.reminderScheduler = ReminderScheduler()
        PATH="/storage/s_gawade/Evee/Multi-LLM-Agent/GLPFT/saved_models/toolbench/Qwen2.5-Coder-7B-Instruct/planner_v2-one-third"
        config = PeftConfig.from_pretrained(PATH)
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
                config.base_model_name_or_path,
                use_fast=False,
        )
        self.llm = llm

    def get_llm_prompt(self):
        """
        Fetch or simulate getting a prescription. This can be modified to fetch data 
        from a file, database, or an API.
        
        :return: A string representing the prescription.
        """
        # Simulating a prescription text input.

        prefix = '''
        You will be given a medical case and the prescription. Now for each case you will have a set of medicines to be taken at specific timings. Now you have to output a JSON that contains exact time at which the medicine is to be taken. Also, give the exact number of days the medicine is to be taken in integer, and the exact time at which the medicine is to be taken in HH:MM in 24 hour format format. Also add the other dosage details or cautions mentioned along with it. Below given is a medial case with the prescription details.

        {
        "medication": {
        "name": "Headache",
        "details": [
        {
        "tablet_name": "Sumatriptan",
        "time": "Once in the morning before breakfast.",
        "dosage": "100 mg",
        "duration": "5 days"
        },
        {
        "tablet_name": "Ibuprofen",
        "time": "Twice a day before breakfast and before dinner",
        "dosage": "200 mg",
        "duration": "5 days"
        }
        ]
        }
        }

        Below is an example of the schedule of medicines.
        {
        "medication_schedule": {
        "medication_name": "Headache",
        "medications": [
        {
        "medicine_name": "Sumatriptan",
        "total_days": 5,
        "timing": ["10:00"],
        "dosage": "100 mg",
        "instructions": "Once in the morning before breakfast."
        },
        {
        "medicine_name": "Ibuprofen",
        "total_days": 5,
        "timing": ["10:00", "21:00"],
        "dosage": "200 mg",
        "instructions": "Twice a day before breakfast and before dinner"
        }
        ]
        }
        }

        Now do the same for another example given below.

        '''

        prompt = prefix + self.prescription
        return prompt

    def postprocess_llm_output(self, llm_output):
        
        start_index = llm_output.find('{')
        end_index = llm_output.rfind('}') + 1

        json_string = llm_output[start_index:end_index]
        print("Json String:", json_string)
        json_object = json.loads(json_string)
        # print(json_object)
        return json_object


    def send_to_llm(self, text):
        """
        Send the prescription to the LLM for processing and obtain structured JSON output.

        :param prescription: The text of the prescription.
        :return: JSON output from the LLM.
        """
        # Simulating LLM response for the given prescription
        # Replace with actual LLM call when integrating.
                
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        inputs = self.tokenizer([text], return_tensors="pt").to("cuda:1")
        
        with self.llm.disable_adapter():
            # output = planner_model.generate(**inputs,max_new_tokens=512)
            output  = self.llm.generate(**inputs, max_new_tokens=512)
            # response = self.llm.process(inputs)
        generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, output)
            ]
        response = self.tokenizer.batch_decode(generated_ids)[0]
        json_response = self.postprocess_llm_output(response)
        return json_response

    def parse_output(self, llm_output):
        """
        Parse the JSON output from the LLM to extract reminders.

        :param llm_output: The JSON output from the LLM.
        :return: A list of reminder dictionaries with time and title.
        """
        reminders = []
        for medication in llm_output["medication_schedule"]["medications"]:
            for time in medication["timing"]:
                reminders.append({
                    "title": f"{llm_output['medication_schedule']['medication_name']} - {medication['medicine_name']} - {medication['dosage']}",
                    "time": time,
                    "duration":  medication["total_days"],
                    "instructions": medication["instructions"],
                })
        return reminders

    def create_reminders(self, reminders):
        """
        Create reminders based on the parsed data. This is a placeholder for reminder scheduling logic.

        :param reminders: A list of reminder dictionaries with time and title.
        """
        for reminder in reminders:
            time = reminder["time"]
            title = reminder["title"]
            instructions = reminder["instructions"]
            no_days = reminder["duration"] #add this also
            time = datetime.strptime(time, '%H:%M').time()
            patient = Patient.objects.get(patient_id=1) #get patient id from user session
            Reminders.objects.create(patient_id=patient, title=title, time=str(time), description=instructions, remaining_days=no_days)
            return {
                "time": time,
                "title": title,
                "instruction": instructions,
            }
            # print("time: ",time, "title: ", title, "instruction: ", instructions )
            #add numberof days also
            # Placeholder for scheduling logic (e.g., system alarm, notification, etc.)
            # self.reminderScheduler.schedule_reminder(reminder_info=reminder)
            # print(f"Reminder scheduled: {title} at {time}. Instructions: {instructions}")


    def run(self):
        """
        Main method to fetch the prescription, process it, and create reminders.
        """
        prompt = self.get_llm_prompt()
        llm_output = self.send_to_llm(prompt)
        print(llm_output)
        reminders = self.parse_output(llm_output)
        print(reminders)
        return self.create_reminders(reminders)


# Example usage
if __name__ == "__main__":
    load_planner_model()
    # run when prescription is uploaded
    prescription = {
            "patientName": "Jane Smith",
            "medications": [
                {
                "medicineName": "Dextromethorphan",
                "dosage": "2 tablets",
                "frequency": "Before each meal",
                "duration": "7 days"
                },
                {
                "medicineName": "Paracetamol",
                "dosage": "500 mg",
                "frequency": "As needed for fever or discomfort",
                "duration": "Until symptoms subside"
                }
            ]
        }
    reminder_manager = ReminderManager(json.dumps(prescription), planner_model)
    reminder_manager.run()
