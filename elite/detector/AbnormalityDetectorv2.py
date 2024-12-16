import pandas as pd
import time
import csv
from eliteapi.models import Patient, PatientVitals

class AbnormalityDetectorWithAveraging:
    def __init__(self, vitals, rest_threshold=20, avg_window=1):
        self.vitals = vitals
        self.rest_threshold = rest_threshold
        self.avg_window = avg_window
        self.last_checked_timestamp = None

    # def calculate_average(self, df, column):
    #     """Calculate the average of the last 'k' values for the given column."""
    #     if len(df) > 0:
    #         return df[column].tail(self.avg_window).mean()
    #     return None

    def detect_abnormality(self, avg_heart_rate, avg_blood_oxygen, steps):
        """Detect abnormal conditions based on the averaged data and steps."""
        steps = int(steps)
        if steps < self.rest_threshold:  # User is resting
            if avg_heart_rate < 50:
                return "Sustained low heart rate detected while resting."
            elif avg_heart_rate > 110:
                return "Sustained high heart rate detected while resting."
            elif avg_blood_oxygen < 90:
                return "Sustained low blood oxygen level detected."
        else:  # User is active
            if avg_heart_rate > 160:
                return "Sustained dangerously high heart rate during activity."
            elif avg_blood_oxygen < 85:
                return "Sustained critically low blood oxygen during activity."
        return None

    def monitor(self):
        """Monitor the vitals and detect abnormalities."""
        print("Abnormality Detector with Averaging Started...")

        heart_rate = self.vitals["heart_rate"]
        oxygen = self.vitals["oxygen"]
        steps = self.vitals["steps"]

        abnormality = self.detect_abnormality(heart_rate, oxygen, steps)
        if abnormality:
            patientobj = Patient.objects.get(patient_id=1)  
            patientVitalsObj = PatientVitals.objects.create(patient_id=patientobj, vitals=self.vitals, softSOS=True)
            # triggerSoftSOS(abnormality, vitals)
            print("Abnormality Detected: ", abnormality)
        return

def detectAbnormality(vitals):
    detector = AbnormalityDetectorWithAveraging(vitals, avg_window=1)
    detector.monitor()