from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
# Create your views here.


@api_view(['POST'])
def Register_Patient(request): 
    
    data = request.data
    try: 
        
        if not data:
            return Response({"error":"User data required"},status=status.HTTP_400_BAD_REQUEST) 
        
        serializer = PatientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Patient registered successfully"},status=status.HTTP_201_CREATED)
        else: 
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    except RuntimeError as e: 
        raise RuntimeError({"error":str(e)})
   
