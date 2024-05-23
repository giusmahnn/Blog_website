from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from .utils import otp_generation
from django.utils import timezone
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        else:
            user = self.model(email=email, password=password, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    '''
    species aditional fields in django built in user creation form
    '''
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    otp_field = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


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