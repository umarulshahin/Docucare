from django.db import models
import uuid
from Authentication_app.models import *



class PatientRecord(models.Model):
    record_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.ForeignKey(Patient_Info, on_delete=models.CASCADE, related_name='patient_info')
    patient_vitals = models.JSONField()
    medical_history = models.JSONField()
    current_condition = models.TextField()
    prescribed_medicines = models.JSONField()
    lab_tests = models.JSONField()
    followup_date = models.DateField(null=True, blank=True)
    doctor_details = models.JSONField()
    hospital_details = models.JSONField()
    insurance_details = models.JSONField()
    additional_notes = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)