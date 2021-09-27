from django.db import models
import uuid
#import the built in django user model
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null=True,blank=True) #connect this model via one to one relation to the inbuilt django's User model
                                                                  #on_delete = models.CASCADE will make sure that any time the user is deleted the profile is deleted
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500,null=True, blank=True)
    short_intro = models.CharField(max_length=900, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True,upload_to='profiles/', default = 'profiles/user-default.png') #upload_to='profiles/' will save the uploaded profile_image by the users into the /static/images/profiles folder
    social_github = models.CharField(max_length=1000, blank=True, null=True)
    social_twitter = models.CharField(max_length=1000, blank=True, null=True)
    social_linkedin = models.CharField(max_length=1000, blank=True, null=True)
    social_youtube = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True , primary_key=True, editable=False) #overriding django unique database items id

    username = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)
