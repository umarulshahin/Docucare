from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid

class PatientManager(BaseUserManager):
    def create_user(self, phone, username, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required")
        user = self.model(phone=phone, username=username, **extra_fields)
        user.set_unusable_password()  
        user.save(using=self._db)
        return user

class Patient_Info(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, blank=False)
    phone = models.CharField(max_length=13, unique=True) 
    gender = models.CharField(max_length=10, blank=False)
    age = models.IntegerField(blank=False)
    place = models.CharField(max_length=100, blank=False)
    date_created = models.DateTimeField(default=timezone.now)

    objects = PatientManager()

    USERNAME_FIELD = "phone"  
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
