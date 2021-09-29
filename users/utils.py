#here in this module we will be overriding the default from django.contrib.auth.tokens import PasswordResetTokenGenerator and rename it to TokenGenerator
from django.contrib.auth.tokens import PasswordResetTokenGenerator

#inorder to use the property is_active of the user we need to import six module from django.utils
import six

class TokenGenerator(PasswordResetTokenGenerator):
    #it is constantly looking out if anything changes
    def _make_hash_value(self,user,timestamp): #override the default method in the PasswordResetTokenGenerator module
        #here we are keeping track of the email is used to activate the account this line is responsible for activating user whem the link is clicked in their respective email addresses
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_active)) #.text_type() creates a new string object from the given object so basically we are converting six into a string object

generated_token = TokenGenerator()
