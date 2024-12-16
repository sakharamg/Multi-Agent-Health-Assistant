from django.db import models

# Create your models here.

# create appointments class
# create soft SOS vitals class
# create symptoms class
# create vitals class
# create patient prescription history class

# class Appointments(models.Model):
#     # appointment id, slot, patient foreign id, doctor id, timestamp, symptoms foreign id, 
    
# class SoftSosVitals(models.Model):
#     # timestamp, patient vitals foreign id, pateint foreign id, symptoms foreign id

# class ReportedSymptoms(models.Model):

class PatientVitals(models.Model):
    # timestamp, patient foreign id, vitals, softSOS T/F, 
    timestamp = models.DateTimeField(auto_now_add=True)
    patient_id = models.ForeignKey(
        "Patient", on_delete=models.CASCADE)
    vitals = models.JSONField()
    softSOS = models.BooleanField(default=False)

class Patient(models.Model):
    # patient id, name, age
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()

class Reminders(models.Model):
    # reminder id, patient id foreign key, title, description, time, remaining days
    reminder_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey("Patient", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    remaining_days = models.IntegerField(default=0)

# class Summary(models.Model):
    # summary id, patient id, date, 

# class PrescriptionHistory(models.Model):
#     #patient id, timestamp, prescription, doctor id