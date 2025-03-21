from django.urls import path
from Authentication_app.views import *
from Patient_app.views import *

urlpatterns = [
    
    
    path('register_patient/',Register_Patient,name='register_patient'),
    path('get_patient_details/',Get_Patient_Details,name='get_patient_details'),
]
