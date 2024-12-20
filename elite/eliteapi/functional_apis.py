import spacy
import json
import os 

nlp = spacy.load("en_core_web_trf")

def retrieve_past_complaints(history):
    past_complaints =[
        {
            "result": [
                {
                    "date": "2023-08-01",
                    "symptoms": "headaches and dizziness",
                    "diagnosis": "migraine"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-07-15",
                    "symptoms": "frequent coughing and shortness of breath",
                    "diagnosis": "asthma"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-06-20",
                    "symptoms": "nausea and vomiting",
                    "diagnosis": "food poisoning"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-05-25",
                    "symptoms": "muscle pain and fatigue",
                    "diagnosis": "flu"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-04-30",
                    "symptoms": "difficulty sleeping and irritability",
                    "diagnosis": "insomnia"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-03-10",
                    "symptoms": "stomach cramps and diarrhea",
                    "diagnosis": "gastroenteritis"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-02-05",
                    "symptoms": "joint pain and swelling",
                    "diagnosis": "arthritis"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-01-20",
                    "symptoms": "persistent cough and fever",
                    "diagnosis": "pneumonia"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-12-15",
                    "symptoms": "blurred vision and headaches",
                    "diagnosis": "glaucoma"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-11-10",
                    "symptoms": "chest pain and shortness of breath",
                    "diagnosis": "heart attack"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-10-05",
                    "symptoms": "skin rash and itching",
                    "diagnosis": "allergic reaction"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-09-30",
                    "symptoms": "unexplained weight loss and fatigue",
                    "diagnosis": "thyroid disorder"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-08-25",
                    "symptoms": "abdominal pain and bloating",
                    "diagnosis": "irritable bowel syndrome"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-07-22",
                    "symptoms": "fever and sore throat",
                    "diagnosis": "strep throat"
                }
            ]
        },
        {
            "result": [
                {
                    "date": "2023-06-15",
                    "symptoms": "numbness and tingling in hands and feet",
                    "diagnosis": "peripheral neuropathy"
                }
            ]
        }
    ]
    similarity = 0
    index = 0
    count = 0
    for complaint in past_complaints:
        doc = nlp(complaint['result'][0]['symptoms'])
        h = nlp(history)
        temp = doc.similarity(h)
        if similarity < temp:
            similarity = temp
            index = count
        count+=1
        
    return json.dumps(past_complaints[index])

def get_available_specialists(history):
    specialists = [
        {
            "specialist_id": "123",
            "name": "Dr. John Smith",
            "specialization": "Cardiologist",
            "available_slot": {
                "date": "2024-11-01",
                "time": "09:00-09:30"
            }
        },
        {
            "specialist_id": "456",
            "name": "Dr. Emily Brown",
            "specialization": "Neurologist",
            "available_slot": {
                "date": "2024-10-15",
                "time": "16:00-16:30"
            }
        },
        {
            "specialist_id": "789",
            "name": "Mr. Michael White",
            "specialization": "Orthopedic Surgeon",
            "available_slot": {
                "date": "2024-09-20",
                "time": "11:00-11:30"
            }
        },
        {
            "specialist_id": "202",
            "name": "Dr. David Kim",
            "specialization": "Gynecologist",
            "available_slot": {
                "date": "2024-07-30",
                "time": "13:00-13:30"
            }
        },
        {
            "specialist_id": "303",
            "name": "Ms. Jessica Wong",
            "specialization": "Physiotherapist",
            "available_slot": {
                "date": "2024-06-10",
                "time": "15:00-15:30"
            }
        },
        {
            "specialist_id": "505",
            "name": "Dr. Maria Garcia",
            "specialization": "Psychiatrist",
            "available_slot": {
                "date": "2024-04-20",
                "time": "17:00-17:30"
            }
        },
        {
            "specialist_id": "606",
            "name": "Mr. William Johnson",
            "specialization": "Radiologist",
            "available_slot": {
                "date": "2024-03-15",
                "time": "12:00-12:30"
            }
        },
        {
            "specialist_id": "707",
            "name": "Dr. Olivia Nguyen",
            "specialization": "Oncologist",
            "available_slot": {
                "date": "2024-02-28",
                "time": "18:00-18:30"
            }
        },
        {
            "specialist_id": "808",
            "name": "Ms. Sophia Patel",
            "specialization": "General Practitioner",
            "available_slot": {
                "date": "2024-01-22",
                "time": "09:30-10:00"
            }
        },
        {
            "specialist_id": "909",
            "name": "Dr. Henry Chen",
            "specialization": "Endocrinologist",
            "available_slot": {
                "date": "2024-12-15",
                "time": "14:30-15:00"
            }
        },
        {
            "specialist_id": "100",
            "name": "Dr. Emma Harris",
            "specialization": "Dermatologist",
            "available_slot": {
                "date": "2024-11-10",
                "time": "11:30-12:00"
            }
        },
        {
            "specialist_id": "110",
            "name": "Mr. Alexander Scott",
            "specialization": "Surgeon",
            "available_slot": {
                "date": "2024-10-05",
                "time": "08:30-09:00"
            }
        },
        {
            "specialist_id": "120",
            "name": "Dr. Isabella Martinez",
            "specialization": "Ophthalmologist",
            "available_slot": {
                "date": "2024-09-30",
                "time": "16:30-17:00"
            }
        }
    ]
    similarity = 0
    index = 0
    count = 0
    for specialist in specialists:
        doc = nlp(specialist['specialization'])
        h = nlp(history)
        temp = doc.similarity(h)
        if similarity < temp:
            similarity = temp
            index = count
        count+=1
        
    return json.dumps(specialists[index])

def confirm_appointment():
    """Confirms an appointment slot and stores it in the hospital's database."""
    return "{'result': True}"

def save_appointement_history():
    
    """Saves appointment information in the user's database for later reference and recurring use cases.""" 
    pass

