from django.contrib import admin
from django.urls import path


from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UsersRegisterUser.as_view(), name='user_register'),

    path('activate/<uidb64>/<token>/', views.UsersActivateUser.as_view(), name='user_activate'),
    path('forgot/', views.UsersForgotPassword.as_view(), name='forgot_password'),
    path('reset/<uidb64>/<token>/', views.UsersResetPassword.as_view(), name='reset_password'),

    path('<uuid:pk>/', views.UsersViewProfile.as_view(), name='view_profile'),
    path('<uuid:pk>/get/', views.get_profile, name='get_profile'),
    path('<uuid:pk>/change_password/', views.change_password, name='change_password'),

]