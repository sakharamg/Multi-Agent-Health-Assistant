from datetime import datetime
from summarizer.summary import Summarizer
from .utils import watchSimulator
from detector.AbnormalityDetectorv2 import detectAbnormality
import json

def healthManager():

    # watch simulator
    vitals = watchSimulator()
    print(vitals)

    # detector
    detectAbnormality(vitals)
    print("All is well")

    # summarizer
    summary_time = datetime.time(hour=21, minute=0, second= 0)
    if is_near_summary_time(summary_time):
        send_daily_summary(patient_id=1) 
    

    # Reminder
    handleReminder()


def handleReminder():
    
    # Calculate the start and end times based on the time threshold
    patient_id = 1
    time_threshold_minutes = 30
    start_time = (datetime.datetime.now() - timedelta(minutes=time_threshold_minutes)).time()
    end_time = (datetime.datetime.now() + timedelta(minutes=time_threshold_minutes)).time()
    
    # Filter the Reminders objects based on patient_id and time range
    reminders = Reminders.objects.filter(
        patient_id=patient_id,
        time__gte=start_time,
        time__lte=end_time
    )

    remindUsers(reminders)
    # reminders.delete() #chamge this to decrease the remaining days and delete only when the remaining days is 0
    for reminder in reminders:
        if reminder.remaining_days == 1:
            reminder.delete() 
        else:
            reminder.remaining_days -= 1
            reminder.save()  
    return


def remindUsers(reminders):
    for reminder in reminders:
        message = f"Reminder: {reminder.title}\nDescription: {reminder.description}"
        send_message_to_user(reminder.patient_id, message)
    return 

def send_daily_summary(patient_id):
    # Code to send the daily summary to users
    # csv_file_path = "daily_data.csv"
    # output_json_path = "averages.json"
    summarizer = Summarizer()
    summary = summarizer.calculate_averages()
    structured_summary = "Summary of the day: " json.dumps(summary, indent=4)
    abnormal_activity = "Detected abnormal activities: "
    send_
    # send the summary to patient
    return


def is_near_summary_time(summary_time, threshold_minutes=30):
    current_time = datetime.datetime.now().time()
    summary_datetime = datetime.datetime.combine(datetime.date.today(), summary_time)
    current_datetime = datetime.datetime.combine(datetime.date.today(), current_time)
    
    time_diff = abs((summary_datetime - current_datetime).total_seconds() / 60)
    
    return time_diff <= threshold_minutes
