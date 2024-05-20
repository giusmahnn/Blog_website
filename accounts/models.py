from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    '''
    species aditional fields in django built in user creation form
    '''
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username