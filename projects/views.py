from django.shortcuts import render

'''this is a inbuilt django Views class that handles the remdering of views that are built in to the django web framework'''
from django.views.generic import View

# Create your views here.
class Home(View):
    #this class will be responsible for showing the developer page
    def get(self, request):
        return render(request, 'home.html')
