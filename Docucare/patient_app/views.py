from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from Authentication_app.models import *
from Authentication_app.serializer import *

@api_view(['GET'])
def Get_Patient_Details(request): 
    
    phone = request.data
    
    try: 
        
        if not phone: 
            return Response({"error":"Phone number required"},status=status.HTTP_400_BAD_REQUEST)
                    
        patient = Patient_Info.objects.filter(phone = phone['phone']).first()
        print(patient,'patient')
        if not patient:   
            return Response({"error":"Phone number does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PatientSerializer(patient)
        token = RefreshToken.for_user(patient)
    
        return Response({"success": {"user":serializer.data,"token":str(token)}},status=status.HTTP_200_OK)
            
    except RuntimeError as e: 
        raise RuntimeError({"error":str(e)})