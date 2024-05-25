from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from .utils import otp_generation
from django.utils import timezone
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        we make use of  class to handle and manage our user creation,
        returns an error if no email is provided. if provided it goes
        ahead to create our user, saves it and returns our saved user
        """
        if not email:
            raise ValueError("Email is required")
        else:
            user = self.model(email=email, password=password, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        This method creates a super user and gives it certain permission.
        """
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

    USERNAME_FIELD = "username" # required field for login
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def save_otp(self):
        """
        This function method uses self to save data in our db,
        the otp_field generates a random number and converts to strings,
        the created_at is a varible to hold the current time the otp was generted
        the self.save saves the data in our db
        """
        self.otp_field= str(otp_generation()) # calls the roandom otp num
        self.otp_created_at= timezone.now() # stores the time it was generated
        self.save()

    def valid_otp(self):
        """
        This function retirvies the current time and then checks if it is less than 100 mins
        If it is less than 10mins it returns true meaning otp is valid and false meaning that,
        it is more than 10 mins and not valid.
        """
        now = timezone.now()
        if self.otp_created_at and now(now - self.otp_created_at).total_seconds() < 600:
            return True
        return False    
    
    
    
    
    def __str__(self):
        return self.username