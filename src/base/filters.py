import django_filters
from .models import *

class ServicesFilter(django_filters.FilterSet):
	class Meta:
		model = Services
		fields = ['title']

class SectorsFilter(django_filters.FilterSet):
	class Meta:
		model = Sectors
		fields = ['title']

class typeFilter(django_filters.FilterSet):
	class Meta:
		model = Types
		fields = ['title']

class ProjectsFilter(django_filters.FilterSet):

	CHOICES = (
		('ascending','Ascending'),
		('descending','Descending'),
	)

	ordering = django_filters.ChoiceFilter(label='Ordering Values', choices=CHOICES, method='filter_by_order')
	
	class Meta:
		model = Projects
		fields = {
			'title':['icontains'],
			'company':['icontains'],

		}

	def filter_by_order(self, queryset, name, value):
		expression = 'created' if value == 'ascending' else '-created'
		return queryset.order_by(expression)

class ProjectGalleryFilter(django_filters.FilterSet):
	class Meta:
		model = projectGallery
		fields = ['project']		