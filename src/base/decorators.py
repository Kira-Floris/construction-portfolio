from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def role_required(allowed_roles=[]):
	def decorator(func):
		def wrap(request, *args, **kwargs):
			if request.user.role in allowed_roles: 
				return func(request, *args, **kwargs)
			else:
				return redirect('forbidden_403')

		return wrap
	return decorator