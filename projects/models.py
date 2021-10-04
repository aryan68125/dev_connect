from django.db import models

import uuid

from users.models import Profile #import Profile model from users moddels.py file
# Create your models here.
class Project(models.Model):

    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE) #ForeignKey stablishes one to many relationship #-> by doing this we are gonna connect a project to the user that actually had created it
    tags = models.ManyToManyField('Tag', blank=True) #setting many to many relationship between tags and the Project model in the database the Tag model is below the Project model that's why we are putthing Tag inside the '' like this 'Tag'
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    title = models.CharField(max_length=200)
    discription = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000,null=True, blank=True)
    source_link = models.CharField(max_length=2000,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True , primary_key=True, editable=False) #overriding django unique database items id

    #models for user uploaded files
    featured_image = models.ImageField(null=True, blank=True, default="default.png")

    def __str__(self):
        return self.title

    #sort the projects by date
    # ordering = ['created']  will give us the oldest entry in the database model first so in order to get the newest first we need to invert that
    class Meta:
        ordering = ['-vote_ratio', '-vote_total' , 'title'] # ordering = ['-created'] will give the newest entry in our database first

    #get all the voters for a specific project i wanna get all the owner's ids here
    @property #-> @property allows us to run a function as an attribute of the Profile model and not as an actual method of the Profile model
    def riviewers(self):
        #get a queryset of all the people that voted on this project
        #and now we will go into the value list in our riview model
        #now make sure that this is a simple list of ids and no objects are present here to do that use flat=True
        queryset = self.riview_set.all().values_list('owner__id', flat=True)
        return queryset     

    #this method is gona run a calculation and update the actual riview count
    @property #-> @property allows us to run a function as an attribute of the Profile model and not as an actual method of the Profile model
    def getVoteCount(self):
         riviews = self.riview_set.all()  #get all the riviews
         print(str(riviews))
         upVotes = riviews.filter(value='up').count()  #get all the upvotes
         print('upVotes: ', upVotes)
         #now get the total number of votes
         totalVotes = riviews.count() #will get the total number of riviews
         print('totalVotes: ', totalVotes)
         ratio = (upVotes/totalVotes) * 100
         #update vote_ratio and vote_total in the database
         self.vote_total = totalVotes
         self.vote_ratio = ratio
         self.save() #update the instance of this vote_total and vote_ratio

class Riview(models.Model):
    VOTE_TYPE = (

         ('up' , 'Up Vote'),
         ('down' , 'Down Vote'),

    )
    owner = models.ForeignKey(Profile, on_delete= models.CASCADE, null=True) #attaching owner to this riview model so we know exactly who commented on who's project
    project = models.ForeignKey(Project, on_delete=models.CASCADE) #ForeignKey stablishes one to many relationship
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices = VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True , primary_key=True, editable=False) #overriding django unique database items id

    #bind project and owner to each other so that we can ensure that a user can only leave one riview on each project
    #by doing this we can never have an riview in the database that have the same owner to the same projecct
    class Meta:
        unique_together = [['owner' , 'project']]

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True , primary_key=True, editable=False) #overriding django unique database items id

    def __str__(self):
        return self.name
