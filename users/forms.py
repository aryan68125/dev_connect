#this form  will generate django's inbuilt model forms in our template so here we define what fields to show in our front end and we can also customize our model forms over here
from django.forms import ModelForm
from django.contrib.auth.models import User
#here in this forms.py file we want to create a form for User's profile that's the reason we are importing Profile model from models.py file in our users application
from . models import Profile, Skill

#creating a modelform for Profile model
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        #fields= '__all__' #this list all the fields that we specified in the models.py file in class Profile
        fields = ['name', 'username', 'email', 'short_intro', 'bio',
            'profile_image', 'social_github', 'social_twitter', 'social_linkedin', 'social_website',
            'location',
        ]
    #customizing our ProfileModel form
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'}) #adding a class input to each of the input fields html in Profile modelForm that was provided to us by django

#creating a model form for Skill model
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        #fields= '__all__' #this list all the fields that we specified in the models.py file in class Profile
        # fields = ['name', 'discription']
        fields = '__all__'
        exclude = ['owner'] #it will render out all the input fields in the template from the skill's model form excluding owner
    #customizing our ProfileModel form
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'}) #adding a class input to each of the input fields html in Profile modelForm that was provided to us by django
