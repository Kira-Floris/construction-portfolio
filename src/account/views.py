from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
import threading
from django.views.generic import ListView, UpdateView
from .tokens import account_activation_token
from .models import *

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from base.decorators import role_required

LOGIN_URL = settings.LOGIN_URL

admin_level = ['Admin']
manager_level = ['Admin', 'Manager']
staff_level = ['Admin', 'Manager', 'Staff']

# Create your views here.

class EmailThread(threading.Thread):
	def __init__(self, email_message):
		self.email_message = email_message
		threading.Thread.__init__(self)

	def run(self):
		self.email_message.send()

@login_required(login_url=LOGIN_URL)
@role_required(allowed_roles=admin_level)
def registerUser(request):
	form = UserRegisterForm()

	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'Activate Your Site Account'
			message = render_to_string('account/emails/account_activation_email.html',{
					'user':user,
					'domain': current_site.domain,
					'uid':urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
				})
			email_message = EmailMessage(
					subject,
					message,
					settings.EMAIL_HOST_USER,
					[user.email]
				)
			EmailThread(email_message).start()
			messages.success(request, ('Please Confirm your email to complete registration.'))
			return redirect('login')
	context = {
		'form':form
	}
	return render(request, 'account/register.html', context)

@login_required(login_url=LOGIN_URL)
@role_required(allowed_roles=staff_level)
def ActivateAccount(request, uidb64, token, *args, **kwargs):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.email_verified = True
		user.save()
		login(request, user)
		messages.success(request, ('Your account have been confirmed. Please continue adding more details about your account.'))
		return redirect('profile')
	else:
		messages.warning(request, ('The confirmation link was invalid, possible because it has already been used'))
		return redirect('login')

def loginUser(request):
	form = UserLoginForm()
	if request.method=='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		getUser = User.objects.get(username__iexact=username)
		if getUser and getUser.email_verified==False:
			messages.warning(request, ('Email is not validated yet, go to your email and validate it'))
			return redirect('login')
		if user is not None:
			login(request, user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			return redirect('dashboard')
		else:
			messages.warning(request, ('User does not exist, or the credentials you entered are wrong'))
			return redirect('login')
	context = {
		'form':form,
	}
	return render(request, 'account/login.html', context)

@login_required(login_url=LOGIN_URL)
@role_required(allowed_roles=staff_level)
def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url=LOGIN_URL)
@role_required(allowed_roles=staff_level)
def profileUser(request):
	if request.method == 'POST':
		if request.user.role != 'Admin':
			form = UserUpdateForm(request.POST,
			 					request.FILES,
			 					instance=request.user)
		else:
			form = AdminUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your account has been updated!')	
			return redirect('profile')
	else:
		if request.user.role != 'Admin':
			form = UserUpdateForm(instance=request.user)
		else:
			form = AdminUpdateForm(instance=request.user)

	context = {
		'form':form,
		'user':request.user,
	}

	return render(request, 'account/profile.html', context)

@login_required(login_url=LOGIN_URL)
@role_required(allowed_roles=staff_level)
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, 'Password was reset successfully.')
			return redirect('profile')
		else:
			return redirect('password_change')
	else:
		form = PasswordChangeForm(user=request.user)

	context = {'form':form}
	return render(request, 'account/password_change.html', context)

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
@method_decorator(role_required(allowed_roles=admin_level), name='dispatch')
class usersListView(ListView):
	model = User
	template_name = 'account/users.html'
	context_object_name = 'users'
	fields = '__all__'

@login_required(login_url=LOGIN_URL)
@role_required(allowed_roles=admin_level)
def userUpdate(request, pk):
	user = User.objects.get(id=pk)
	form = UserAdminForm(instance=user)
	if request.method == 'POST':
		form = UserAdminForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
			messages.success(request, 'User updated successfully!')
			return redirect('users')


	context = {
		'user': user,
		'form': form,
	}
	return render(request, 'account/user.html', context)

@login_required(login_url=LOGIN_URL)
@role_required(allowed_roles=admin_level)
def userDelete(request, pk):
	user = User.objects.get(id=pk)
	if request.method == 'POST':
		 user.delete()
		 messages.success(request, 'User have been deleted')
		 return redirect('users')

	context = {'user':user}
	return render(request, 'account/user_delete.html', context)

@login_required(login_url=LOGIN_URL)
@role_required(allowed_roles=admin_level)
def webInfoCreate(request):
	webinfo = WebInfo.objects.first()
	form = WebInfoForm(instance=webinfo)
	if request.method == 'POST':
		if WebInfo.objects.all().count()==1:
			form = WebInfoForm(request.POST, request.FILES, instance=webinfo)
			if form.is_valid():
				form.save()
				messages.success(request, 'Website Info Updated')
				return redirect('webinfo')
		elif WebInfo.objects.all().count() > 1:
			messages.success(request, 'Website info already exceeds 1')
		else:
			form = WebInfoForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				messages.success(request, 'Website Info Registered')
				return redirect('webinfo')
	context={
		'form': form
	}
	return render(request, 'account/webinfo.html', context)
	