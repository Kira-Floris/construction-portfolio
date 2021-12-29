from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as __
from account.models import User

# Create your models here.

def services_upload_path(instance, filename):
    return 'images/services/{0}.jpeg'.format(instance.title)

class Services(models.Model):
    class Meta:
        verbose_name_plural = 'Services'

    title = models.CharField(max_length=100, null=False, blank=False, unique=True)
    image = models.ImageField(upload_to=services_upload_path)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Sectors(models.Model):
    class Meta:
        verbose_name_plural = 'Sectors'

    title = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Types(models.Model):
    class Meta:
        verbose_name_plural = 'Types'
        verbose_name = 'Type'

    title = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
        
def project_directory_path(instance, filename):
    return 'images/projects/{0}/{1}.jpeg'.format(instance.title, instance.title)

class Projects(models.Model):
    class Meta:
        verbose_name_plural = 'Projects'
        ordering = ['-date_created']

    title = models.CharField(max_length=100, null=False, blank=False, default="house", unique=True)
    feature = models.ImageField(upload_to=project_directory_path)
    company = models.CharField(max_length=100, default='Cadeaux')
    description = models.TextField()
    value = models.FloatField()
    sector = models.ForeignKey(Sectors, on_delete=models.CASCADE)
    type = models.ForeignKey(Types, on_delete=models.CASCADE)
    services = models.ManyToManyField(Services, blank=False)
    date_created = models.DateTimeField(auto_now_add = True, verbose_name='Date Created')
    date_updated = models.DateTimeField(auto_now = True, verbose_name = 'Last Updated')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

def project_gallery(instance, filename):
    return 'images/projects/{0}/gallery/{1}.jpeg'.format(instance.project, filename)

class projectGallery(models.Model):
    class Meta:
        verbose_name_plural = 'Gallery'

    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=project_gallery)

    def __str__(self):
        return str(self.project) + '(additional images)'