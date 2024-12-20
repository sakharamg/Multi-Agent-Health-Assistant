import random
import time
from datetime import datetime
import csv
from eliteapi.models import PatientVitals, Patient
import easyocr
import re

class SmartwatchSimulator:
    def __init__(self, save_interval=60, output_file="vitals_data.csv"):
        self.steps = 0
        self.total_calories_burned = 0
        self.sleep_data = {"deep": 0, "light": 0, "awake": 0, "rem": 0}
        self.save_interval = save_interval
        self.output_file = output_file
        self.last_save_time = time.time()

    def generate_heart_rate(self):
        """Generate a random heart rate with rare abnormalities."""
        if random.random() < 0.05:
            return random.choice([random.randint(40, 59), random.randint(101, 140)])
        return random.randint(60, 100)

    def generate_blood_oxygen(self):
        """Generate a random SpO2 level with rare abnormalities."""
        if random.random() < 0.03:
            return random.randint(85, 94)
        return random.randint(95, 100)

    def simulate_steps(self):
        """Simulate steps in a random interval."""
        new_steps = random.randint(0, 50)
        self.steps += new_steps
        return self.steps

    def simulate_calories_burned(self):
        """Simulate calories burned based on steps taken."""
        calories_per_step = 0.04
        new_calories = self.steps * calories_per_step
        self.total_calories_burned = round(new_calories, 2)
        return self.total_calories_burned

    def simulate_sleep(self):
        """Simulate sleep data with random durations, including REM sleep."""
        total_sleep_minutes = max(300, min(600, int(random.gauss(450, 60))))  # Gaussian between 5-10 hours
        awake_percentage = random.uniform(5, 10)  # Awake is 5-10%
        rem_percentage = random.uniform(20, 25)  # REM is 20-25%
        light_percentage = random.uniform(50, 60)  # Light is 50-60%
        deep_percentage = 100 - (awake_percentage + rem_percentage + light_percentage)  # Remaining percentage for Deep

        # Convert percentages to minutes
        awake = int((awake_percentage / 100) * total_sleep_minutes)
        rem = int((rem_percentage / 100) * total_sleep_minutes)
        light = int((light_percentage / 100) * total_sleep_minutes)
        deep = total_sleep_minutes - (awake + rem + light)  # Ensure total matches sleep duration

        self.sleep_data = {"deep": deep, "light": light, "rem": rem, "awake": awake}
        return self.sleep_data

    def display_vitals(self):
        """Generate and display current vitals."""
        heart_rate = self.generate_heart_rate()
        blood_oxygen = self.generate_blood_oxygen()
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Heart Rate: {heart_rate} bpm{' (Abnormal)' if heart_rate < 60 or heart_rate > 100 else ''}")
        print(f"Blood Oxygen Level: {blood_oxygen}%{' (Abnormal)' if blood_oxygen < 95 else ''}")
        print(f"Steps: {self.simulate_steps()}")
        print(f"Calories Burned: {self.simulate_calories_burned()} kcal")
        print(f"Sleep Data (last night): {self.simulate_sleep()} minutes (Deep:Light:REM:Awake)")
        print("-" * 50)
        return heart_rate, blood_oxygen

    def save_vitals(self, vitals):
        
        patient = Patient.objects.all().get(patient_id=1)
        patientVitalsObj = PatientVitals.objects.create(vitals=vitals, patient_id=patient)
        
        
    def get_vitals(self):
        """Get vitals data"""
        data = {
            "oxygen": self.generate_blood_oxygen(),
            "heart_rate": self.generate_heart_rate(),
            "steps": self.simulate_steps(),
            "calories": self.simulate_calories_burned(),
            "sleep": self.simulate_sleep()
        }
        return data

# if __name__ == "__main__":
def watchSimulator():
    simulator = SmartwatchSimulator(save_interval=300)  # Save data every 60 seconds

    print("Smartwatch Simulator with Abnormality Detection Started...")
    vitals = simulator.get_vitals()
    simulator.save_vitals(vitals)
    return vitals
    # try:
        # vitals = simulator.get_vitals()
        # current_time = time.time()
        # simulator.save_vitals(vitals)
        # Save vitals at specified intervals
        # if current_time - simulator.last_save_time >= simulator.save_interval:
            # simulator.save_vitals(vitals)
            # simulator.last_save_time = current_time

        # time.sleep(5)  # Update every 5 seconds
    # except KeyboardInterrupt:
    #     print("\nSimulation stopped.")

def handleFileUpload(f):
    with open("/home/s_gawade/shivam/Multi-Agent-Health-Assistant/elite/media/prescription.jpg", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# Create an OCR reader object
def getPrescriptionOCR(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    string=""
    for detection in result:
        string += " "+detection[1]
    match  = re.search("Prescription", string, re.IGNORECASE)
    processed = string[match.end():]
    match = re.search("Signature", processed, re.IGNORECASE)
    processed = processed[:match.start()]
    return processed

def inferDosagefromOCR(ocr_string: str):
    if "1-0-0" in ocr_string:
        return "Before breakfast"
    elif "0-1-0" in ocr_string:
        return "After lunch"
    elif "0-0-1" in ocr_string:
        return "After dinner"
    elif "1-1-1" in ocr_string:
        return "Before every meal"
    elif "1-0-1" in ocr_string:
        return "After Breakfast and dinner"
    elif "0-1-1" in ocr_string:
        return "After Lunch and dinner"
    elif "1-1-0" in ocr_string:
        return "After breakfast and lunch"
    
def extractSubstring(string, start_tag):
    end_tag = "</" + start_tag[1:]
    start = string.find(start_tag)
    end = string.find(end_tag)
    if start != -1 and end != -1:
        return string[start + len(start_tag) : end]
    else:
        return ""