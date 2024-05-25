from django.contrib import admin
from .models import CustomUser



admin.site.register(CustomUser) # Registers our model to the admin site