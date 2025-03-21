
from rest_framework import serializers
from .models import *
from rest_framework import status
import re
class PatientSerializer(serializers.ModelSerializer): 
    
    class Meta:
        
        model = Patient_Info
        fields = ['username', 'phone', 'gender', 'age', 'place']
        
    def validate(self, attrs):
        
        username_pattern = r'^[A-Za-z][A-Za-z0-9_]{2,}$'
        phone_pattern = r'^\+\d{2}\d{10}$'

        
        if not attrs['username'] or not attrs['phone'] or not attrs['gender'] or not attrs['age'] or not attrs['place']:
            raise serializers.ValidationError('please fill all the fields', status=status.HTTP_400_BAD_REQUEST)
        
        elif not re.match(username_pattern,attrs['username']):
            raise serializers.ValidationError({"username":"Username must start with a letter and be at least 3 characters long, containing only letters, numbers, or underscores."})
        elif not re.match(phone_pattern,attrs['phone']):
            raise serializers.ValidationError({"phone":"Enter a valid phone number"})
        elif Patient_Info.objects.filter(phone = attrs['phone']).exists():
            raise serializers.ValidationError({"phone":"Phone number already exists"})
        return attrs
    def create(self, validated_data):
        return super().create(validated_data)