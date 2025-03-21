from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import *


@api_view(['GET'])
def Get_Patient_Details(request): 
    
    