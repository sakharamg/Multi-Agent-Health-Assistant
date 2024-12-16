from background_task import background
from summarizer.summary import Summarizer
from datetime import datetime

@background(schedule=datetime(hour=0, minute=0, second=0)) 
def send_daily_summary(patient_id):
    # Code to send the daily summary to users
    csv_file_path = "daily_data.csv"
    output_json_path = "averages.json"
    summarizer = Summarizer(csv_file_path, output_json_path)
    summarizer.calculate_averages()
    
    # Add your code here to send the summary to users
    # For example, you can use Django's email functionality to send the summary via email