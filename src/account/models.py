from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as __
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib import admin
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

# Creating a Custom User Model

ROLES = {
    ('Admin', 'Admin'),
    ('Manager', 'Manager'),
    ('Staff','Staff'),
}

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, role, password, **other_fields):
        if not email:
            raise ValueError('enter a valid email')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name, last_name=first_name, role=role, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, role, password, **other_fields):
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser=True')

        if role!='Admin':
            raise ValueError('superuser must have role of Admin')

        return self.create_user(username, email, first_name, last_name, role, password, **other_fields)

def profile_upload_path(instance, filename):
    return 'images/profiles/{0}.jpeg'.format(instance.username)

class UserObject(models.Manager):
    def get_queryset(self):
        return super(UserObject, self).get_queryset().filter(display=True).exclude(position='Staff')
        
class User(AbstractUser):
    profile = models.ImageField(upload_to=profile_upload_path)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    email_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.TextField()
    role = models.CharField(max_length=15, choices=ROLES, default='Staff')
    position = models.CharField(max_length=150, default='Staff')
    display = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'role']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def save(self, *args, **kwargs):
        if self.is_superuser==True:
            self.role='Admin'
            self.is_staff=self.is_active=True
        if self.role=='Admin':
            self.is_superuser=self.is_staff=self.is_active=True
        super().save(*args, **kwargs)

    home_users = UserObject()


def logo_upload_path(instance, filename):
    return 'image/business/{0}'.format(filename)

class WebInfo(models.Model):
    name = models.CharField(__('Enter your business Name'),max_length=150)
    image = models.ImageField(upload_to=logo_upload_path)
    email = models.EmailField(__('Enter a business email'), default=settings.EMAIL_HOST_USER)
    telephone = PhoneNumberField(unique=True)
    instagram = models.CharField(max_length=150, unique=True)
    facebook = models.CharField(max_length=150, unique=True)
    twitter = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name 

    def save(self, *args, **kwargs):
        if WebInfo.objects.all().count() >= 1: 
            if self._state.adding:
                raise ValueError("Information already exists")
            else:
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)