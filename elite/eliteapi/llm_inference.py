import transformers
from peft import PeftModel, PeftConfig, PeftMixedModel
import json
import torch
PATH="/home/jagdish/storage/Multi-LLM-Agent/GLPFT/saved_models/toolbench/Qwen2.5-Coder-7B-Instruct/planner_v2-one-third"
config = PeftConfig.from_pretrained(PATH)

tokenizer = transformers.AutoTokenizer.from_pretrained(
        config.base_model_name_or_path,
        use_fast=False,
)

planner_model = transformers.AutoModelForCausalLM.from_pretrained(
    config.base_model_name_or_path,
    device_map="cuda:1"
)
planner_model = PeftModel.from_pretrained(planner_model, PATH)
# planner_model= planner_model.merge_and_unload()
# planner_model.disable_adapters()
# for n,p in planner_model.named_parameters():
#     if "lora" in n:
#         print(n)

# planner_model.load_adapter(PATH, "planner")
# planner_model.set_adapter("planner")

for n,p in planner_model.named_parameters():
    if "lora" in n:
        print(n)

# planner_model.disable_adapters()


text = """
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

        Case 1: Cough and Cold

        {
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
        "frequency": "Before breakfast",
        "duration": "4 days"
        }
        ]
        }
"""


messages = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
    {"role": "user", "content": text}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
inputs = tokenizer([text], return_tensors="pt").to("cuda:1")

# inputs = tokenizer(text, return_tensors="pt").to("cuda:1")

with planner_model.disable_adapter():
    output = planner_model.generate(**inputs,max_new_tokens=512)

generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, output)
    ]
response = tokenizer.batch_decode(generated_ids)[0]

print(response)


