#this signal file is responsible for connecting our Profile model to our django's inbuilt User model
#in order for this signals.py file to work you need to add this signal.py file to users/apps.py file
'''
in apps.py file
under the name = 'users'
add the following lines of code
def ready(self):
    import users.signals
'''

#importing django signals to handle user creation and deletion events

#post_save is gonna trigger anytime a model is saved already and after the fact that it's saved
#post_delete is gonna trigger anytime a model is deleted
from django.db.models.signals import post_save, post_delete
#import a decorator
from django.dispatch import receiver

#import the built in django user model
from django.contrib.auth.models import User

#import Profile model from models.py of the users application of this django project
from . models import Profile

#handeling Registration, email verification and login of the users this website
#create a function for the django signals
#this function is the reciever function
#sender = model that sends the signal, instance = the instance of the model that actually triggered this ,
#created = this is gonna let us know if the user or a model was added to the database or if it was simply saved again Note: it is a True or False value
#now configuring our sender signal post_save.connect(Function_name_that_you_want_to_trigger, sender = Model_name_that_will_be_sending_that_signal)
#post_save.connect(profileUpdated, sender = Profile) so basically you can achieve same create/update functionality by simply using @reciever(type_of_the_signal, sender = Model_name_that_will_be_sending_that_signal)
@receiver(post_save, sender = User)
def CreateProfile(sender, instance, created, **kwargs):
    print('CreateProfile Triggered')
    #check if this is a first instance of the user (if the user just created his/her profile for the first time on this website)
    if created == True:
        user = instance #instance is the instance of the sender of the signal
        profile = Profile.objects.create( #create a user profile and have a copy of that in the Profile model connecting inbuilt User model for auth and registration to the Profile model for the user
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        ) #create a profile

#handeling user_profile delete function
#now configuring our sender signal post_delete.connect(Function_name_that_you_want_to_trigger, sender = Model_name_that_will_be_sending_that_signal)
#post_delete.connect(deleteUser, sender=Profile) so basically you can achieve same delete functionality by simply using @reciever(type_of_the_signal, sender = Model_name_that_will_be_sending_that_signal)
#delete the user from django's inbuilt User model for auth and registration if admin deletes the user from Profile model
@receiver(post_delete, sender = Profile)
def deleteUser(sender, instance, **kwargs):
    print('deleteUser Triggered')
    try:
        user = instance.user # the instance here is the Profile model and it will get the user from the profile model
        user.delete() #this will delete the user from the User django's inbuilt model
    except:
        print("An exception occurred") 
