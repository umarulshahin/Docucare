from rest_framework import serializers 
from .models import *
from rest_framework import status

class MedicalRecordSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = PatientRecord
        fields = ['record_id', 'patient_id', 'patient_vitals', 'medical_history', 'current_condition', 'prescribed_medicines', 'lab_tests', 'followup_date', 'doctor_details', 'hospital_details', 'insurance_details', 'additional_notes', 'date_created' ]
    
    def validate(self, attrs):
         
        # validate all fields 
        if  not attrs['patient_id'] or not attrs['patient_vitals'] or not attrs['medical_history'] or not attrs['current_condition']  or not attrs['followup_date'] or not attrs['doctor_details'] or not attrs['hospital_details'] or not attrs['insurance_details'] or not attrs['additional_notes']:
            
            raise serializers.ValidationError('please fill all the fields', status=status.HTTP_400_BAD_REQUEST)
        
        return attrs
    
    def create(self, validated_data):
        return super().create(validated_data)