from django.shortcuts import render

from django.http import HttpResponse

from . models import Project
# Create your views here.

def projects(request):
    projects = Project.objects.all()
    data_for_front_end = {
        'projects' : projects,
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
