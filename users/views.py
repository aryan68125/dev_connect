from django.shortcuts import render

#import the profile model
from . models import Profile

# Create your views here.
def profiles(request):
    profiles = Profile.objects.all() #get all the profiles that are present in the database
    stuff_for_front_end = {
        'profiles':profiles,
    }
    return render(request, 'users/profiles.html', stuff_for_front_end)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    # now here what we want is to show the skills with a discription differently than the skills that do not have the discription
    #exclude(discription__exact="") exclude is like a filter but it inverts the result that would normally be produced by the filter
    #it will exclude any skill that do not have any discription
    #here we are getting the skills that have discription
    topSkills = profile.skill_set.exclude(discription__exact="")

    #here we are getting every skill that do not have a discription
    otherSkills = profile.skill_set.filter(discription="")

    stuff_for_front_end={
        'profile':profile,
        'topSkills':topSkills,
        'otherSkills':otherSkills,
    }
    return render(request, 'users/user-profile.html', stuff_for_front_end)
