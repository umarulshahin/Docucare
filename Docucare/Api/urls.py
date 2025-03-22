from django.urls import path
from Authentication_app.views import *
from Patient_app.views import *

urlpatterns = [
    
    
    path('register_patient/',Register_Patient,name='register_patient'),
    path('get_patient_details/',Get_Patient_Details,name='get_patient_details'),
    path('store_patient_medical_records/',Store_patient_Medical_Records,name='store_patient_medical_records'),
    path('organize_patient_data/',Organize_Patient_Data,name='organize_patient_data'),
]
