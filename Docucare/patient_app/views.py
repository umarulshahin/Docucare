from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from Authentication_app.models import *
from Authentication_app.serializer import *
from rest_framework.permissions import IsAuthenticated
import environ
import google.generativeai as genai
import whisper
import os
import tempfile
from whisper.audio import load_audio




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
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Organize_Patient_Data(request): 
    
    # configure gemini api 
    
    env = environ.Env()
    genai.configure(api_key=env('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-2.0-flash')

    text = request.data.get('text')
    id = request.data.get('id')
    
    if not id: 
        return Response({"error":"Patient id required"},status=status.HTTP_400_BAD_REQUEST)
    if not text: 
        return Response({"error":"Text required"},status=status.HTTP_400_BAD_REQUEST)
    
    # getting parient details and medical records
    
    patient = Patient_Info.objects.filter(id = id).first()
    patient_medical = PatientRecord.objects.filter(patient_id = id)
    
    if not patient:
            return Response({"error":"Patient not found"}, status=status.HTTP_404_NOT_FOUND)
            
    
    serializer_medical = MedicalRecordSerializer(patient_medical,many=True)
    serializer_patient = PatientSerializer(patient)

   
    prompt = f"""
            You are a medical data processing assistant. Generate a structured medical report by combining the following information:

            PATIENT INFORMATION:
            {serializer_patient.data}

            UNSTRUCTURED MEDICAL TEXT:
            "{text}"

            Structure the output as a JSON object with the following schema:
            {serializer_medical.data}
            Format the output as a well-structured medical summary in paragraph form.

            Important guidelines:
            1. DO NOT include any introductory or concluding sentences like "Here's a medical report..." or similar phrases.
            2. DO NOT include any patient IDs, record IDs, or other technical identifiers in your response.
            3. Focus only on clinically relevant information (symptoms, diagnosis, treatment, etc.).
            4. Use proper medical terminology while ensuring the text is clear and well-structured.
            5. Include patient username, demographics, vitals, medical history, current condition, prescribed medicines, lab tests, follow-up date, and doctor details in a cohesive narrative.
            6. If any information cannot be determined, make reasonable medical assumptions based on available data.
            7. DO NOT include any metadata or structured fields—write only in paragraph form.
            """

        
    try: 
        
        response = model.generate_content(prompt)        
        
        if response.text is None:
            return Response({"error":"Failed to generate medical report"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        print(response.text,'response')
                
            # Create or update generated medical report in database

        medical_report = MedicalReport.objects.filter(patient_id=id).first()
        
        if medical_report: 
            serializer = MedicalReportSerializer(medical_report,data={'report':response.text},partial=True)
        else: 
            serializer = MedicalReportSerializer(data={'patient_id':id,'report':response.text})
        
        if serializer.is_valid(): 
            serializer.save()
            return Response({"success":"Medical Report generated successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        
    except Exception as e: 
        
        print(f"Error processing medical text: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Process_Audio_Records(request): 

    file_path = request.FILES.get('audio')
    id = request.data.get('id')
    
    try: 
        
        if not file_path: 
            return Response({"error":"Audio file required"},status=status.HTTP_400_BAD_REQUEST)
        elif not id: 
            return Response({"error":"Patient id required"},status=status.HTTP_400_BAD_REQUEST)
        
                # Create a temporary file with the correct extension
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, f"temp_audio.{file_path.name.split('.')[-1]}")
        
        with open(temp_path, 'wb+') as destination:
            for chunk in file_path.chunks():
                destination.write(chunk)
            
            # Load the audio file using whisper load audio
        audio = load_audio(temp_path)
        
        model = whisper.load_model("base.en")
        result = model.transcribe(audio)
        
            #After convering audio Clean up the temporary file
        os.remove(temp_path)
        os.rmdir(temp_dir)                
        
            # Create or update the medical report in the database using the generated text from the audio recording.
        medical_report = MedicalReport.objects.filter(patient_id=id).first()
        
        if medical_report: 
            serializer = MedicalReportSerializer(medical_report,data={'report':result['text']},partial=True)
        else: 
            serializer = MedicalReportSerializer(data={'patient_id':id,'report':result['text']})
        
        if serializer.is_valid(): 
            serializer.save()
            return Response({"success":"Medical Report generated successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)    
        
    except RuntimeError as e: 
        raise RuntimeError({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)    