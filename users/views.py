from django.shortcuts import render, redirect

#import the profile model
from . models import Profile

#--------------------------USER REGISTRATION, LOGIN, AUTHENTICATION,LOGOUT RELATED IMPORTS STARTS HERE----------------------------------
#for our login page to have proper login and user authaentication process we have to make these imports below
from django.contrib.auth import login, authenticate, logout

#import the built in django user model
from django.contrib.auth.models import User

'''this is a inbuilt django Views class that handles the remdering of views that are built in to the django web framework'''
from django.views.generic import View

'''install validate-email module before importing it type pip3 install validate-email in your terminal to install the module'''
from validate_email import validate_email

'''
construct a url that is unique to the application that we've built so we need the the current domain that our application is running on
and we will set it dynamically we can import this:- from django.contrib.sites.shortcuts import get_current_site
'''
from django.contrib.sites.shortcuts import get_current_site

#now redirect user to the login page
# so inorder to do that you need to import :- from django.template.loader import render_to_string this library renders a template with a context automatically
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from . utils import generated_token
from django.core.mail import EmailMessage
from django.conf import settings

#import UserCreationForm built in django register form for register page
from django.contrib.auth.forms import UserCreationForm

#----------------------reset password----------------------
from django.contrib.auth.tokens import PasswordResetTokenGenerator
#----------------------reset password----------------------


#--------------------------USER REGISTRATION, LOGIN, AUTHENTICATION,LOGOUT RELATED IMPORTS ENDS HERE----------------------------------

#import django message library for displaying messages to the user on the website
from django.contrib import messages

#-------------------------USER Registration, EMAIL VERIFICATION , LOGIN AND LOGOUT FUNCTIONALITY STARTS HERE--------------------------------

class RegistrationView(View):
    #to handle the get request
    def get(self, request):
        #Restrict the user who is already logged in from seeing the login page
        if request.user.is_authenticated:
            return redirect('profiles')
        return render(request, 'users/register.html')

    def post(self, request):
        #now we need to go back to the template register otherwise we won't be able to create th user in the database
        data = request.POST
        stuff_for_frontend = {

              'data' : data,
              'has_error':False,

        }

        #now check if the passwords are provided
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password)<6:
            messages.add_message(request,messages.ERROR, 'Password should be atleast 6 characters long')
            stuff_for_frontend['has_error'] = True
        #check if the both password and password2 are matching or not
        if password!= password2:
            messages.add_message(request,messages.ERROR, "Password don't match")
            stuff_for_frontend['has_error'] = True

        #now we need to validate the email address entered by the user so inorder to do that we need to install validate-email module from pip repository
        #type pip3 install validate-email in your terminal
        email = request.POST.get('email')
        #now check if the email address is valid or not
        if not validate_email(email):
            messages.add_message(request,messages.ERROR, 'Email not valid!')
            stuff_for_frontend['has_error'] = True

        #check if the email is taken
        #to find out if the user exsists or not in our database if yes then return user name taken use .exists() function to do the job
        if User.objects.filter(email=email).exists():
            messages.add_message(request,messages.ERROR, 'Email is taken')
            stuff_for_frontend['has_error'] = True
        #now check if there is any error in the user input
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            messages.add_message(request,messages.ERROR, 'Username is taken')
            stuff_for_frontend['has_error'] = True

        print(data)
        if stuff_for_frontend['has_error']:
            return render(request, 'users/register.html', stuff_for_frontend, status=400) #here if we set status to 400 that meands we can prevent the user profile from being created in the database if the error is generated if any of our test condition fails


        #now create the user in the database
        user = User.objects.create_user(username=username, email=email)
        #now set the password for that user and store it in the database
        user.set_password(password)
        #set active user to false so that they don't accidentally get logged in before the email verification process is complete
        user.is_active=False
        #now save the user
        user.save() # now we can say that the user account is successfully created
        #now add a message informing the user that their account has been created successfully
        messages.add_message(request,messages.SUCCESS, 'Account is created successfully')
        messages.add_message(request,messages.SUCCESS, 'Activation link is sent check your email')

        #send the verification link to the user's email address
        #step1. construct a url that is unique to the application that we've built so we need the the current domain that our application is running on
        #       and we will set it dynamically we can import this:- from django.contrib.sites.shortcuts import get_current_site
        current_site = get_current_site(request) #get_current_site(request) will give us the current domain of our website dinamically
        #step2. create an email subject
        email_subject= 'Email verification'

        #step3. construct a message
        # so inorder to do that you need to import :- from django.template.loader import render_to_string this library renders a template with a context automatically
        #convert the user.pk into bytes so we need to import:- from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
        #import a module that generated a unique token for our application when we need to verify the user's email address :- from django.contrib.auth.tokens import PasswordResetTokenGenerator it can be used to activate accounts and to reset password
        create_a_context_for_front_end={
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generated_token.make_token(user),
        }
        message = render_to_string('users/activate.html',create_a_context_for_front_end)
        #step4. send an email for authentation of the account import :- from django.core.mail import EmailMessage and import settings :- from django.conf import settings
        '''
        email_message = EmailMessage(
           email_subject,            #subject of the email
           message,                  #message that you want to send via email
           settings.EMAIL_HOST_USER, #EMAIL_HOST = 'smtp.gmail.com' that is being imported from the settings.py of the django project
           [email],                  #email adderess entered by the user in the regitration form in the front end of the application of the django project
        )
        '''
        email_message = EmailMessage(
           email_subject,
           message,
           settings.EMAIL_HOST_USER,
           [email],
        )
        email_message.send()
        #now redirect user to the login page
        return redirect('login')

class ActivateAccountView(View):
    def get(self, request,uidb64,token):
        print(f"request = {request}")
        #in here we will check if the token is valid or not
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(f"uid = {uid}")
            #do not use User.objects.filter(pk=uid).exists(): instead use User.objects.get(pk=uid) otherwise when you
            #deploy your application on heroku it will throuw an exception
            user = User.objects.get(pk=uid)
            print(f"user = {user}")
        except User.DoesNotExist:
            user = None

        #now check the user before activating them
        if user is not None and generated_token.check_token(user,token):
            print(f"token = {token}")
            #now activate the user in the database for operational ready i.e user now have the permission to use the web Application
            user.is_active = True
            print(f"user active stauts = {user.is_active}")
            user.save()
            messages.add_message(request,messages.INFO,'account activated successfully')
            return redirect('login')
        return render(request,'users/error.html', status=401)



#create a view for the login page
def loginUser(request):
    #Restrict the user who is already logged in from seeing the login page
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #check if the username is already in the database or not
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'usename does not exist!')
            print('usename does not exist!')

        user = authenticate(request, username=username, password=password) #if it finds the username and password in the database then its gonna return that user otherwise it will return none

        #now we will check if we got the user in the database or not
        if user is not None:
            #if user exists then go ahead and log the user in to this website
            login(request, user) #this function will create a session for the user in the database in that sessions table
            #if the user successfully logs in then go ahead and redirect the user to his/her respective account
            return redirect('profiles')

        else: # if the user in None i.e the user exist in the database but either the password or the username do not match from the database then tell the user that either the username or password is incorrect
            print('username or password is incorrect')
            messages.error(request,'usename or password is incorrect')

    return render(request, 'users/login_register.html')

#logout function
def logoutUser(request):
    logout(request) #this is django's inbuilt function to logout user from the website
    #now we can redirect user to the login page of our website
    messages.error(request,'User was logged out')
    return redirect('login')


#--------------reset password related views starts here-----------------
class RequestResetEmailView(View):
    #here we are gonna have a from where user can supply their email address
    def get(self, request):
        return render(request, 'users/request-reset-email.html')

    #here we will handle the post request from request-reset-email.html page
    def post(self,request):
        email = request.POST['email']

        #before we send the mail to this email address we need to check if this user even exist in our database
        if not validate_email(email): #step1. check the email is valid or not
            messages.add_message(request,messages.INFO,'email address not valid!')
            return render(request, 'users/request-reset-email.html')

        user = User.objects.filter(email=email) #this will find the user having the email address entered in the provide email section of the reset passsword html page
        if user.exists():
            # this will return true if the user is already in our website's database
            #send the verification link to the user's email address
            #step1. construct a url that is unique to the application that we've built so we need the the current domain that our application is running on
            #       and we will set it dynamically we can import this:- from django.contrib.sites.shortcuts import get_current_site
            current_site = get_current_site(request) #get_current_site(request) will give us the current domain of our website dinamically
            #step2. create an email subject
            email_subject= 'Reset password'

            #step3. construct a message
            # so inorder to do that you need to import :- from django.template.loader import render_to_string this library renders a template with a context automatically
            #convert the user.pk into bytes so we need to import:- from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
            #import a module that generated a unique token for our application when we need to verify the user's email address :- from django.contrib.auth.tokens import PasswordResetTokenGenerator it can be used to activate accounts and to reset password
            create_a_context_for_front_end={
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]), #here we won't use the utils.py file to generate a token here we will use an inbuilt class to generate a token to set a new password
            }
            message = render_to_string('users/reset-user-password.html',create_a_context_for_front_end)
            #step4. send an email for authentation of the account import :- from django.core.mail import EmailMessage and import settings :- from django.conf import settings
            '''
            email_message = EmailMessage(
               email_subject,            #subject of the email
               message,                  #message that you want to send via email
               settings.EMAIL_HOST_USER, #EMAIL_HOST = 'smtp.gmail.com' that is being imported from the settings.py of the django project
               [email],                  #email adderess entered by the user in the regitration form in the front end of the application of the django project
            )
            '''
            email_message = EmailMessage(
               email_subject,
               message,
               settings.EMAIL_HOST_USER,
               [email],
            )
            email_message.send()


        messages.add_message(request,messages.INFO,'email reset link has been sent to your email address')
        return render(request, 'users/request-reset-email.html')

class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        #send uidb64 and token  to the set-new-password.html via context dictionary
        context = {
            'uidb64':uidb64,
            'token':token,
        }

        #prevent user from using the same token that was sent in the email of the user to reset the password
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token): #if this returns false then the link is already used to reset the password
                messages.add_message(request,messages.INFO,'Password reset link expired')
                return redirect('login')

        except DjangoUnicodeDecodeError as identifier:
            messages.add_message(request,messages.INFO,'Oops something went wrong!')
            return render(request, 'users/set-new-password.html',context)

        return render(request, 'users/set-new-password.html', context)

    #handeling the post requests
    def post(self, request, uidb64, token):
        #send uidb64 and token  to the set-new-password.html via context dictionary
        context = {
            'uidb64':uidb64,
            'token':token,
            'has_error': False,
        }

        #check the password
        password1 = request.POST.get('password_1')
        password2 = request.POST.get('password_2')
        if len(password1) < 6:
            messages.add_message(request,messages.INFO,'password must be atleast 6 characters long')
            context['has_error'] = True
        if password1 != password2:
            messages.add_message(request,messages.INFO,'password do not match')
            context['has_error'] = True
        if context['has_error'] == True:
            return render(request, 'users/set-new-password.html',context)

        #if the user entered the correct password then we are going to proceed with setting the new password for the user account
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password1)
            user.save()
            messages.add_message(request,messages.INFO,'password changed successfully')
            return redirect('login')
        except DjangoUnicodeDecodeError as identifier:
            messages.add_message(request,messages.INFO,'Oops something went wrong!')
            return render(request, 'users/set-new-password.html',context)

        return render(request, 'users/set-new-password.html',context)



#-------------------------USER Registration, EMAIL VERIFICATION , LOGIN AND LOGOUT FUNCTIONALITY ENDS HERE--------------------------------





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
