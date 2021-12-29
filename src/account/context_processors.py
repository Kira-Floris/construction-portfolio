from .models import WebInfo
from base.models import projectGallery

def extras(request):
	webInfo = WebInfo.objects.first()
	return {'webinfo': webInfo}

def gallery(request):
	gallery = projectGallery.objects.all()
	return {'galleryPhotos': gallery}