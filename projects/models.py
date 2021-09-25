from django.db import models

import uuid

# Create your models here.
class Project(models.Model):
    tags = models.ManyToManyField('Tag', blank=True) #setting many to many relationship between tags and the Project model in the database the Tag model is below the Project model that's why we are putthing Tag inside the '' like this 'Tag'
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    title = models.CharField(max_length=200)
    discription = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000,null=True, blank=True)
    source_link = models.CharField(max_length=2000,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True , primary_key=True, editable=False) #overriding django unique database items id

    def __str__(self):
        return self.title

class Riview(models.Model):
    VOTE_TYPE = (

         ('up' , 'Up Vote'),
         ('down' , 'Down Vote'),

    )
    #owner =
    project = models.ForeignKey(Project, on_delete=models.CASCADE) #ForeignKey stablishes one to many relationship
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices = VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True , primary_key=True, editable=False) #overriding django unique database items id

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True , primary_key=True, editable=False) #overriding django unique database items id

    def __str__(self):
        return self.name
