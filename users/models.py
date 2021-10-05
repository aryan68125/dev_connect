from django.db import models
import uuid

#import the built in django user model
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null=True,blank=True) #connect this model via one to one relation to the inbuilt django's User model
                                                                  #on_delete = models.CASCADE will make sure that any time the user is deleted the profile is deleted
    name = models.CharField(max_length=200, blank=True, null=True) #name is set from User model via signals here we renamed First_name in User model to name in the Profile model
    email = models.EmailField(max_length=500,null=True, blank=True)
    short_intro = models.CharField(max_length=900, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True,upload_to='profiles/', default = 'profiles/user-default.png') #upload_to='profiles/' will save the uploaded profile_image by the users into the /static/images/profiles folder
    social_github = models.CharField(max_length=1000, blank=True, null=True)
    social_twitter = models.CharField(max_length=1000, blank=True, null=True)
    social_linkedin = models.CharField(max_length=1000, blank=True, null=True)
    social_website = models.CharField(max_length=1000, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True , primary_key=True, editable=False) #overriding django unique database items id

    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.username)

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True) #whenever a user profile gets deleted the skills will also be deleted so Profile model is the parent of this Skill model
    name = models.CharField(max_length=200, blank=True, null=True)
    discription = models.TextField(blank=True, null=True) #discription of the skill
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True , primary_key=True, editable=False) #overriding django unique database items id

    def __str__(self):
        return str(self.name)

class Message(models.Model):
    #models.SET_NULL will not delete the mseesages sent by the sender user if the sender user decides to delete the account it will still show the message sentr by the sender user to the recipient user
    sender = models.ForeignKey(Profile, on_delete= models.SET_NULL, null=True, blank=True) #person sending the message
    recipient = models.ForeignKey(Profile, on_delete= models.SET_NULL, null=True, blank=True, related_name = "messages") #person getting the message related_name = "messages" allows us to connect both sender and recipient to the Profile model without any issue without it we would not be allowed to connect them to the Profile model both at the same time
    name = models.CharField(max_length = 200, null=True, blank=True) #get the string value of the user

    #email related attributes
    subject = models.CharField(max_length = 200, null=True, blank=True) #get the string value of the user
    email = models.EmailField(max_length = 200, null=True, blank=True) #get the string value of the user
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True) #any messages that you haven't opened up yet will be shown at the top
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True , primary_key=True, editable=False) #overriding django unique database items id

    def __str__(self):
        return self.subject

    #set the ordering of the messages
    class Meta:
        ordering = ['is_read', '-created']
