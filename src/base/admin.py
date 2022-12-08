from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea 
from .models import *

# Register your models here.

models = [Services, Sectors, Types, Projects, projectGallery, Team]

for model in models:
    admin.site.register(model)

