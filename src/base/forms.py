from django.forms import ModelForm
from django import forms
from django.forms.models import inlineformset_factory
from phonenumber_field.formfields import PhoneNumberField
from .models import *

projectGalleryFormset = inlineformset_factory(Projects, projectGallery, fields=('image',), extra=7)

class ContactForm(forms.Form):
    from_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter your email'}),required=True)
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Subject'}),required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Your message...'}), required=True)

class ProjectsForm(ModelForm):
	if Services.objects.all().count() > 0:
		services = forms.ModelMultipleChoiceField(
			queryset=Services.objects.all(),
			widget=forms.CheckboxSelectMultiple,
			required=True,)
	else:
		services = None

	class Meta:
		model = Projects
		exclude = ['created_by']

class ServicesForm(ModelForm):
	class Meta:
		model = Services
		exclude = ['created_by']

class SectorsForm(ModelForm):
    class Meta:
       model = Sectors
       exclude = ['created_by'] 

class TypesForm(ModelForm):
	class Meta:
		model = Types
		exclude = ['created_by']

class TeamForm(ModelForm):
	class Meta:
		model = Team
		fields = '__all__'
