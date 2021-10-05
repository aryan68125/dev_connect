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

    #user info account with CRUD functionality for Logged in users
    path('account/', views.userAccount, name = 'account'),
    path('edit-account/', views.editAccount, name = 'edit-account'),

    #url routes related to logged in user's skills
    path('create-skill/', views.createSkill, name = 'create-skill'),
    path('update-skill/<str:pk>/', views.updateSkill, name = 'update-skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill, name = 'delete-skill'),

    #url roputes for messages realted stuff in our website
    path('inbox/', views.inbox, name = 'inbox'),
    path('message/<str:pk>/', views.viewMessage, name = 'message'),
    path('send-message/<str:pk>/', views.createMessage, name = 'send-message'), #here str:pk is required so that we know where to send this message to
]
