from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils import otp_generation
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):
    '''
    species aditional fields in django built in user creation form
    '''
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    otp_field = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)


    def save_otp(self):
        self.otp_field= str(otp_generation())
        self.otp_created_at= timezone.now()
        self.save()

    def valid_otp(self):
        now = timezone.now()
        if self.otp_created_at and now(now - self.otp_created_at).total_seconds() < 600:
            return True
        return False    
    
    
    
    
    def __str__(self):
        return self.username