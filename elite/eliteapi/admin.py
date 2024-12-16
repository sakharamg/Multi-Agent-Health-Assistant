from django.contrib import admin
from .models import PatientVitals, Patient, Reminders
# Register your models here.
admin.site.register(PatientVitals)
admin.site.register(Patient)
admin.site.register(Reminders)