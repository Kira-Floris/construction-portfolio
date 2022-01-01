from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail, EmailMessage,BadHeaderError
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import role_required
from django.contrib import messages
from .filters import *
from .forms import *
from account.models import *

from .models import *

LOGIN_URL = settings.LOGIN_URL

admin_level = ['Admin']
manager_level = ['Admin', 'Manager']
staff_level = ['Admin', 'Manager', 'Staff']

# Create your views here.

"""
VIEWS FOR THE CLIENT SIDE
"""


def home(request):
	projects = Projects.objects.all()
	services = Services.objects.all()
	sectors = Sectors.objects.all()
	users = User.home_users.all()
	context = {
		'projects': projects,
		'services': services,
		'sectors': sectors,
		'users': users,
	}
	return render(request, 'base/client/home.html', context)

def about_us(request):
	users = User.home_users.all()
	context = {
		'users': users,
	}
	return render(request, 'base/client/about_us.html', context)

def projects(request):
	projects = Projects.objects.all()
	gallery = projectGallery.objects.all()
	if projects:
		context = {
			'projects': projects,
			'gallery': gallery
			}
	else:
		context = {'projects': None}
	return render(request, 'base/client/projects.html', context)

def services(request):
	services = Services.objects.all()
	if services:
		context = {'services': services}
	else:
		context = {'services':None}
	return render(request, 'base/client/services.html', context)

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            message = message + "\nFrom: " + from_email
            try:
                send_mail(subject, message, from_email, [settings.EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, ('Thanks '+from_email+', your message has been received.'))
            form = ContactForm()
    return render(request, "base/client/contact.html", {'form': form})


"""
VIEWS FOR THE ADMIN SIDE
"""

@login_required(login_url=LOGIN_URL)
@role_required(allowed_roles=staff_level)
def dashboard(request):
	projects = Projects.objects.all().count()
	services = Services.objects.all().count()
	sectors = Sectors.objects.all().count()
	types = Types.objects.all().count()
	all_users = User.objects.all().count()
	admin = User.objects.filter(role='Admin').count()
	managers = User.objects.filter(role='Manager').count()
	staff = User.objects.filter(role='Staff').count()
	users = {
		'all': all_users,
		'admins': admin,
		'managers': managers,
		'staff': staff,
	}
	context = {
		'projects': projects,
		'services': services,
		'sectors': sectors,
		'types': types,
		'users': users,
	}
	return render(request, 'base/admin/dashboard.html', context)

"""
Services views for admin
"""

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=staff_level), name='dispatch')
class servicesList(ListView):
	model = Services
	template_name = 'base/admin/services.html'
	context_object_name = 'services'
	fields = '__all__'

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class servicesCreate(CreateView):
	model = Services
	template_name = 'base/admin/components/add_service.html'
	form_class = ServicesForm
	success_url = reverse_lazy('servicesList_admin')

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super(servicesCreate, self).form_valid(form)

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class servicesUpdate(UpdateView):
	model = Services
	template_name = 'base/admin/components/add_service.html'
	form_class = ServicesForm
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('servicesList_admin')

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class servicesDelete(DeleteView):
	model = Services
	template_name = 'base/admin/components/delete_service.html'
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('servicesList_admin')

"""
Sectors views for admin
"""

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=staff_level), name='dispatch')
class sectorsList(ListView):
	model = Sectors
	template_name = 'base/admin/sectors.html'
	context_object_name = 'sectors'
	fields = '__all__'

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class sectorsCreate(CreateView):
	model = Sectors
	template_name = 'base/admin/components/add_sector.html'
	form_class = SectorsForm
	success_url = reverse_lazy('sectorsList_admin')

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super(sectorsCreate, self).form_valid(form)

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class sectorsUpdate(UpdateView):
	model = Sectors
	template_name = 'base/admin/components/add_sector.html'
	form_class = SectorsForm
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('sectorsList_admin')

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class sectorsDelete(DeleteView):
	model = Sectors
	template_name = 'base/admin/components/delete_sector.html'
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('sectorsList_admin')

"""
Category views for admin
"""

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=staff_level), name='dispatch')
class typeList(ListView):
	model = Types
	template_name = 'base/admin/types.html'
	context_object_name = 'types'
	paginate_by = 10
	fields = '__all__'

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class typesCreate(CreateView):
	model = Types
	template_name = 'base/admin/components/add_type.html'
	form_class = TypesForm
	success_url = reverse_lazy('typesList_admin')

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super(typesCreate, self).form_valid(form)

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class typesUpdate(UpdateView):
	model = Types
	template_name = 'base/admin/components/add_type.html'
	form_class = TypesForm
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('typesList_admin')

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class typesDelete(DeleteView):
	model = Types
	template_name = 'base/admin/components/delete_type.html'
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('typesList_admin')

"""
Projects views for admin
"""

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=staff_level), name='dispatch')
class projectsList(ListView):
	model = Projects
	template_name = 'base/admin/projects.html'
	context_object_name = 'projects'
	fields = '__all__'
	paginate_by = 20
	filterset_class = ProjectsFilter

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class projectsCreate(CreateView):
	model = Projects
	template_name = 'base/admin/components/add_project.html'
	form_class = ProjectsForm
	success_url = reverse_lazy('projectsList_admin')

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super(projectsCreate, self).form_valid(form)

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=staff_level), name='dispatch')
class projectsDetail(DetailView):
	model = Projects
	template_name = 'base/admin/project.html'
	pk_url_kwarg = 'pk'
	fields = '__all__'
	context_object_name = 'project'

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class projectsUpdate(UpdateView):
	model = Projects
	template_name = 'base/admin/components/add_project.html'
	form_class = ProjectsForm
	pk_url_kwarg = 'pk'
	
	def form_valid(self, form):
		form.save()
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('projectsDetail_admin', kwargs={'pk':self.object.pk})

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class projectsDelete(DeleteView):
	model = Projects
	template_name = 'base/admin/components/delete_project.html'
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('projectsList_admin')


"""
project gallery views for admin
"""

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=manager_level), name='dispatch')
class projectGalleryEdit(SingleObjectMixin, FormView):
	model = Projects
	template_name = 'base/admin/project-gallery.html'
	context_object_name = 'project'

	def get(self, request, *args, **kwargs):
		self.object = self.get_object(queryset=Projects.objects.all())
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object(queryset=Projects.objects.all())
		return super().post(request, *args, **kwargs)

	def get_form(self, form_class=None):
		return projectGalleryFormset(**self.get_form_kwargs(), instance=self.object)

	def form_valid(self, form):
		form.save()
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('projectsDetail_admin', kwargs={'pk':self.object.pk})

@login_required(login_url=LOGIN_URL)
@role_required(allowed_roles=staff_level)
def forbidden_403(request):
	return render(request, 'forbidden_403.html')

def handler404(request, exception):
	return render(request, 'notFound.html')

def handler500(request):
	return render(request, 'serverError.html')