from django.shortcuts import render, redirect

from django.http import HttpResponse

from . models import Project, Tag

#now indorder to use a model form that we jsut created in the forms.py we are just gonna import it into our views.py
from .forms import ProjectForm

#restrict unauthenticated user from seeing add project page
#we won't be using mixins here because we are using function based views mixins are used when using class based views when foloowing standard procedures for django web development
#instead we will be using login_required decorator to ristrict unauthenticated users from acessing certain pages in our website
from django.contrib.auth.decorators import login_required

#import searchProject.py file here so that we can search projects in the projects_list.html page
from . searchProject import searchProject

#paginators import it will allow us to create a multi page website
#PageNotAnInteger, EmptyPage will allow us to set the page number to 1 when the user first go to our projects page
#in other words page 1 will be shown to the user when he/she opens up the project_list.html page for the first time
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

def projects(request):
    projects , search_query = searchProject(request) #search projects (query set)

    #PAGE PAGINATION STARTS HERE
    #setting up the pages in our project_list.html page
    #request.GET.get('page') will get the page number that we are currently on from the frontend
    page = request.GET.get('page') #give us the first page of these results
    results = 6 #give us 6 projects(results) per page
    paginator = Paginator(projects, results) #paginator = Paginator(query set , results ) go ahead an paginate the project query set and give us the results here

    try:
        #now paginate the project list page
        #now reset the projects variable and index it by a specific page only get 6 results (projects)
        #here we are defining what page do we wanna get from this query set
        #so here we will be getting 6 projects and we are gonna get the first page those 6 projects
        projects = paginator.page(page)
    #the page will not be passed in when the user first enters the projects_list page
    except PageNotAnInteger: #if page is not passed in then it will come to this block
        page=1
        projects = paginator.page(page)
    #if user tries to go to a page number that does not exists using url links in the browser then we should prevent our website from crashing
    #paginator.num_pages will tell us how many pages we have
    except EmptyPage:
        page = paginator.num_pages #if the user goes out of bounds or exceeds the max number of pages that are actually present in the project_list.html page then go ahead and give us the last page
        projects = paginator.page(page)

    #right now in this current state pagination will produce 100 buttons if qwe have 100 pages in our website but we don't want that
    #we want to limit the number of buttons shown at the bottom of the page to 5 so we need to somehow create a range or rolling window for our page button in pagination

    leftIndex = int(page) - 2 #the page that is on our left side
    #leftIndex is gonna return -ve if we are on page 3 as you know 3-4=-1 so we need to avoid that from happening
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 3 #far right page
    #here we need to avoid creating extra buttons for next page if we are already at the last page here let me give an example
    #if a user is at page 15 and 15th page is the last page then we should avoid making more page buttons from 15 to 20
    #as 16 to 20 page do not exist in this senario so we need to avoid this
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages +1

    custom_range = range(leftIndex,rightIndex)
    #PAGE PAGINATION ENDS HERE

    data_for_front_end = {
        'projects' : projects,
        'search_query':search_query,
        'paginator':paginator,
        'custom_range':custom_range
    }
    return render(request, 'projects/projects_list.html', data_for_front_end)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()

    data_for_front_end = {
        'projectObj':projectObj,
        'tags':tags,
    }
    return render(request, 'projects/single-project.html', data_for_front_end)

#resitrict unauthenticated users from acessing add project page in our website
#@login_required(login_url='pass the url to redirect unauthenticated user to the login page')
#this view function will create a model form for us for creating a project in the project app in django
@login_required(login_url='login')
def createProject(request):
    #here we will connect the newly created project to its authenticated(logged in user) user who actually created it using create-project link in the Add project button in their respective user accounts
    #so by doing this every project will have an owner in this case it will be the logged in or authenticated user in current time
    profile = request.user.profile  #get the logged in user

    # here we will create a form that will be generated by the model form in the forms.py file by the class ProjectForm...
    form = ProjectForm()

    if request.method == 'POST':
        #for debugging
        print(request.POST)
        form = ProjectForm(request.POST, request.FILES) #request.FILES will get the images uploaded by the users from the front end and now the links of those images can be saved in the database
        if form.is_valid(): #save the form data if the form is valid and it will add the newly created object to the database
            project = form.save(commit=False) #it is gonna give us the instance of the current project

            #here we are setting the currently logged in user to this newly created project as an owner of that particular project
            project.owner = profile #and then we can go into that project instance and update the owner attribute of that newly created project owner is the oneToMany relationship
            project.save() #now finally re save the newly created project into our database
            return redirect('account')

    data_for_front_end = {
         'form':form,
    }
    return render(request, "projects/project_form.html", data_for_front_end)

#create an update view and here we are gonna reuse the model form from form.py file that we created inside our projects application in our django project
@login_required(login_url='login')
#if a user1 is logged in as a user and if that user1 knows the id of the project of user2 then he could just copy paste the link of that user2's project
#and edit the project him self and we need to stop that from happening
def updateProject(request, pk):
    #prevent user1 from acessing user2's projects via url route link (unique project link) in edit projects page
    profile = request.user.profile

    #profile.project_set is gonna return only the set of projects that the logged in user owns
    #now if a user1 tries to visit a url route that leads him to a project owned by user2 in the edit projects page then
    #project = profile.project_set.get(id=pk) is gonna prevent user1 from going to that route
    project = profile.project_set.get(id=pk) #here we are gonna get the project from the database that has the id matching to the primary key that is passed from the front end
    # here we will create a form that will be generated by the model form in the forms.py file by the class ProjectForm
    form = ProjectForm(instance = project) #the only difference between createView and updateView is we are gonna pass in an instance
                         #so an instance is gonna be the project that we are gonna edit

    if request.method == 'POST':
        #for debugging
        print(request.POST)
        form = ProjectForm(request.POST , request.FILES , instance = project) # here pass request.POST along with what project are we updating at the moment instance = project
        if form.is_valid(): #save the form data if the form is valid and it will add the newly created object to the database
            form.save()
            return redirect('account')

    data_for_front_end = {
         'form':form,
    }
    return render(request, "projects/project_form.html", data_for_front_end)

#create a function for deleting a project in the projects application of this django project
#if a user1 is logged in as a user and if that user1 knows the id of the project of user2 then he could just copy paste the link of that user2's project
#and delete the project him self and we need to stop that from happening
@login_required(login_url='login')
def deleteProject(request, pk):
    #prevent user1 from acessing user2's projects via url route link (unique project link) in delete projects page
    profile = request.user.profile
    #profile.project_set is gonna return only the set of projects that the logged in user owns
    #now if a user1 tries to visit a url route that leads him to a project owned by user2 in the delete projects page then
    #project = profile.project_set.get(id=pk) is gonna prevent user1 from going to that route
    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete() #delete the project from the database
        return redirect('account')
    data_for_front_end ={
        'object':project,
    }
    return render(request, "delete_template.html", data_for_front_end)
