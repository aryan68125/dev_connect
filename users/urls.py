from django.urls import path
from . import views

urlpatterns = [
    #login,logout and registration url routes
    path('login/', views.loginUser, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    #class based views for registration, email verification, password reset via email verification
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    path('request-reset-email', views.RequestResetEmailView.as_view(), name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>', views.SetNewPasswordView.as_view(), name='set-new-password'),

    path('', views.profiles, name = 'profiles'),
    path('profile/<str:pk>/', views.userProfile, name = 'user-profile'),
]
