from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from Authentication_app.models import *
from Authentication_app.serializer import *
from rest_framework.permissions import IsAuthenticated


# ........................ Get Patient Details and Generate jwt token .........................
@api_view(['GET'])
def Get_Patient_Details(request): 
    
    phone = request.data
    
    try: 
        
        if not phone: 
            return Response({"error":"Phone number required"},status=status.HTTP_400_BAD_REQUEST)
                    
        #get patient dippend on phone number 
        
        patient = Patient_Info.objects.filter(phone = phone['phone']).first()
        
        if not patient:   
            return Response({"error":"Phone number does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PatientSerializer(patient)
        
        # generate jwt token using patient details 
        
        token = RefreshToken.for_user(patient)
    
        return Response({"success": {"user":serializer.data, "token":{"refresh":str(token),"access":str(token.access_token)}}},status=status.HTTP_200_OK)
            
    except RuntimeError as e: 
        raise RuntimeError({"error":str(e)})
    
# ......................... Store Patient Medical Records ...............................
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Store_patient_Medical_Records(request): 
    
    data = request.data 
    
    try: 
        
        serializer = MedicalRecordSerializer(data=data)
        if serializer.is_valid(): 
            serializer.save()
            return Response({"success":"Medical Record stored successfully"},status=status.HTTP_201_CREATED)
        
        else : 
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    except RuntimeError as e: 
        raise RuntimeError({"error":str(e)})
    