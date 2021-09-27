"""devsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

#handeling images uploaded by the user into our website and create a path to find the uploaded images of the users
from django.conf import settings
#this static import will help us create a url for our static files
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),

    path('', include('users.urls')),
]

#added a media url route to this file so that django knows how to fetch user uploaded images for the front end
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#added a STATIC url route to this file so that django knows how to serve static files to the front end when debugging is set to false in the settings.py i.e when we are in a production environment
#the next step is to install a third party package called django white noise
#then type 'whitenoise.middleware.WhiteNoiseMiddkeware' in the middleware sections of settings.py file
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
