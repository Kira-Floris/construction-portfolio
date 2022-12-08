from django.urls import path
from . import views
 

urlpatterns = [

	# client side urls

	path('', views.home, name = "home"),
	path('services/', views.services, name='services_client'),
	path('about_us/', views.about_us, name='about-us'),
	path('projects/', views.projects, name='projects_client'),
	path('contact/', views.contact, name='contact'),

	# authenticated urls

	path('dash/', views.dashboard, name='dashboard'),

	path('dash/team/', views.TeamList.as_view(), name='teamList_admin'),
	path('dash/team/add', views.TeamCreate.as_view(), name='teamCreate_admin'),
	path('dash/team/<int:pk>', views.TeamUpdate.as_view(), name='teamUpdate_admin'),
	path('dash/team/delete/<int:pk>', views.TeamDelete.as_view(), name='teamDelete_admin'),

	path('dash/services/', views.servicesList.as_view(), name='servicesList_admin'),
	path('dash/services/add', views.servicesCreate.as_view(), name='servicesCreate_admin'),
	path('dash/services/<int:pk>', views.servicesUpdate.as_view(), name='servicesUpdate_admin'),
	path('dash/services/delete/<int:pk>', views.servicesDelete.as_view(), name='servicesDelete_admin'),

	path('dash/sectors/', views.sectorsList.as_view(), name='sectorsList_admin'),
	path('dash/sectors/add', views.sectorsCreate.as_view(), name='sectorsCreate_admin'),
	path('dash/sectors/<int:pk>', views.sectorsUpdate.as_view(), name='sectorsUpdate_admin'),
	path('dash/sectors/delete/<int:pk>', views.sectorsDelete.as_view(), name='sectorsDelete_admin'),
	
	path('dash/types/', views.typeList.as_view(), name='typesList_admin'),
	path('dash/types/add', views.typesCreate.as_view(), name='typesCreate_admin'),
	path('dash/types/<int:pk>', views.typesUpdate.as_view(), name='typesUpdate_admin'),
	path('dash/types/delete/<int:pk>', views.typesDelete.as_view(), name='typesDelete_admin'),

	path('dash/projects/', views.projectsList.as_view(), name='projectsList_admin'),
	path('dash/projects/add', views.projectsCreate.as_view(), name='projectsCreate_admin'),
	path('dash/project/<int:pk>', views.projectsDetail.as_view(), name='projectsDetail_admin'),
	path('dash/projects/update/<int:pk>', views.projectsUpdate.as_view(), name='projectsUpdate_admin'),
	path('dash/projects/delete/<int:pk>', views.projectsDelete.as_view(), name='projectsDelete_admin'),

	path('dash/projects/<int:pk>/gallery/', views.projectGalleryEdit.as_view(), name='projectGalleryEdit_admin'),

	path('dash/forbidden_403/', views.forbidden_403, name='forbidden_403'),
] 
