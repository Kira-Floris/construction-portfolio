from django.urls import path
from . import views

urlpatterns = [
	path('register/', views.registerUser, name='register'),
	path('activate/<uidb64>/<token>/', views.ActivateAccount, name='activate'),
	path('login/', views.loginUser, name='login'),
	path('logout/', views.logoutUser, name='logout'),
	path('profile/', views.profileUser, name='profile'),
	path('password_change/', views.change_password, name='password_change'),
	path('users/', views.usersListView.as_view(), name='users'),
	path('user/<str:pk>', views.userUpdate, name='user_update'),
	path('user/delete/<str:pk>', views.userDelete, name='user_delete'),
	path('webinfo/', views.webInfoCreate, name='webinfo'),
]