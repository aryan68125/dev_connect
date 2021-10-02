#this file will handle the search function to find a developer based on their name , their short_intro and their skills in our developers page

from . models import Profile,Skill

#this import will alllow us to search developers in profiles page using multiple model parameters
from django.db.models import Q

def searchDeveloper(request):
    #setting up search functionality in our profiles.html page
    search_query = '' #this search_query will be passed into the filter that we add band by default we want to make sure that if we don't have any data in the front end then search_query should be an empty string

    #SEARCH A DEVELOPER BASED ON THEIR NAME AND THEIR SHORT INTRO
    #get the data from the front end in the search profile input field so that we can do search operation on the profiles page
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    #now we will search user's (DEVELOPER) based on their skills
    skills = Skill.objects.filter(name__icontains=search_query) #query set for searching skills in the database

    #here filter out the user profiles based on their name name__icontains is used here to make sure that our search is not case sensitive
    #this Q allows us to search developers in profiles page using multiple parameters and '|'(pipe symbol) acts as an or statement between the two Q search quyeries
    # as soon as we added a query set for developer's skill "Q(skill__in =skills )" in order for us to search develloper by his/her skills
    #if we use "Profile.objects.filter()" then this will cause duplicates to occur in our page which should be avoided this is happening because of our Skill model query set
    # so inorder to combat this problem we need to use replace filter() with distinct().filter()
    profiles = Profile.objects.distinct().filter( Q(name__icontains=search_query) |
          Q(short_intro__icontains = search_query) |
          Q(skill__in = skills ) #this skill is an object of Skill model database
    ) #get all the profiles that are present in the database
    return profiles, search_query
