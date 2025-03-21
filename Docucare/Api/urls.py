from django.urls import path
from Authentication_app.views import *

urlpatterns = [
    
    
    path('register_patient/',Register_Patient,name='register_patient'),
]
