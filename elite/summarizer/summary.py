import json
import pandas as pd
from django.db.models import Avg
from datetime import datetime, timedelta

class Summarizer:
    def __init__(self, csv_file_path, output_json_path):
        pass

    def calculate_averages(self):
        current_time = datetime.now()

        # Calculate the time 24 hours ago
        last_24_hours = current_time - timedelta(hours=24)

        # Filter the PatientVitals objects based on patient_id and timestamp
        vitals_last_24_hours = PatientVitals.objects.filter(
            patient_id=patient_id,
            timestamp__gte=last_24_hours
        )

        # Calculate the average of each vital
        oxygen_avg = vitals_last_24_hours.aggregate(Avg('vitals__oxygen'))['vitals__oxygen__avg']
        heart_rate_avg = vitals_last_24_hours.aggregate(Avg('vitals__heart_rate'))['vitals__heart_rate__avg']
        steps_avg = vitals_last_24_hours.aggregate(Avg('vitals__steps'))['vitals__steps__avg']
        calories_avg = vitals_last_24_hours.aggregate(Avg('vitals__calories'))['vitals__calories__avg']

        deep_sleep_avg = vitals_last_24_hours.aggregate(Avg('vitals__sleep__deep'))['vitals__sleep__deep__avg']
        light_sleep_avg = vitals_last_24_hours.aggregate(Avg('vitals__sleep__light'))['vitals__sleep__light__avg']
        rem_sleep_avg = vitals_last_24_hours.aggregate(Avg('vitals__sleep__rem'))['vitals__sleep__rem__avg']
        awake_avg = vitals_last_24_hours.aggregate(Avg('vitals__sleep__awake'))['vitals__sleep__awake__avg']



        average_vitals = { 
        'oxygen': oxygen_avg,
        'heart_rate': heart_rate_avg,
        'steps': steps_avg,
        'calories': calories_avg,
        'sleep': {
            'deep': deep_sleep_avg,
            'light': light_sleep_avg,
            'rem': rem_sleep_avg,
            'awake': awake_avg
        }
        }

        return average_vitals

    def get_abnormal_patient_vitals(self):
        # Get all abnormal vitals for the past 24 hours
        current_time = datetime.now()

        # Calculate the time 24 hours ago
        last_24_hours = current_time - timedelta(hours=24)

        # Filter the PatientVitals objects based on patient_id and timestamp
        vitals_last_24_hours = PatientVitals.objects.filter(
            patient_id=patient_id,
            timestamp__gte=last_24_hours,
            softSOS=True
        )

        vitals_json = [x.vitals for x in vitals_last_24_hours]

        return vitals_json



# # Example usage
# csv_file_path = "daily_data.csv"
# output_json_path = "averages.json"
# summarizer = Summarizer(csv_file_path, output_json_path)
# summarizer.calculate_averages()