from . models import Project, Tag

#this import will alllow us to search developers in profiles page using multiple model parameters
from django.db.models import Q

def searchProject(request):
    #setting up search functionality in our profiles.html page
    search_query = '' #this search_query will be passed into the filter that we add band by default we want to make sure that if we don't have any data in the front end then search_query should be an empty string

    #SEARCH A DEVELOPER BASED ON THEIR NAME AND THEIR SHORT INTRO
    #get the data from the front end in the search profile input field so that we can do search operation on the profiles page
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    #now apply search project by tags
    #get tags from Tag model database
    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
          Q(title__icontains=search_query) |
          Q(discription__icontains=search_query) |
          Q(owner__name__icontains = search_query) |  #owner__name__icontains here owner = parent model of the Project (parent model of Project model is Profile model)
                                                      # so here essentially we are going to owner > name (name of the owner in Profile model) > __icontains which gives us the name if any of the word matches with the models in the database
          Q(tags__in=tags) #so here we are asking django to find us a project that contains a tag that has been entered in the search field in the projects page
    )
    return projects, search_query
