from django.db import models
import re
import bcrypt
# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        #validate whether email already exists in the db
        email_match = User.objects.filter(email = postData['registration_email'])
        if len(email_match) != 0:
            errors['email_exists_already'] = 'The email already exists. Please try a different name'
        
        #validate required fields are filled out
        if len(postData['registration_first_name']) == 0:
            errors['first_name_req'] = 'First name is required'
        if len(postData['registration_last_name']) == 0:
            errors['last_name_req'] = 'Last name is required'
        if len(postData['registration_email']) == 0:
            errors['email_req'] = 'Email is required'
        if len(postData['registration_password']) == 0:
            errors['password_req'] = 'Password is required!'

        #validate email pattern
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['registration_email']):    # test whether a field matches the pattern            
            errors['email_pattern'] = "Invalid email address!"
        
        #validate field length requirements are met
        if len(postData['registration_first_name']) < 2:
            errors['first_name_length'] = 'First name must be at least 2 characters'
        if len(postData['registration_last_name']) < 2:
            errors['last_name_length'] = 'Last name must be at least 2 characters'
        if len(postData['registration_password']) < 8:
            errors['registration_password_length'] = 'Password must be at least 8 characters'
        
        #validate passwords match
        if postData['registration_password'] != postData['registration_confirm_password']:
            errors['registration_password_match'] = 'Passwords must match'


        return errors

####################################################################

    def login_validator(self, postData):
        errors = {}
        #validate email matches records
        email_match = User.objects.filter(email = postData['login_email'])
        if len(email_match) == 0:
            errors['invalid_email_login'] = 'Email does not exist. Please try a different email'
        
        #validate required fields are filled out
        if len(postData['login_email']) == 0:
            errors['email_required'] = 'Email is required'

        if len(postData['login_password']) == 0:
            errors['password_required'] = 'Password is required'

        #validate whether password matches
        if bcrypt.checkpw(postData['login_password'].encode(), email_match[0].password.encode()):
            pass
        else:
            errors['incorrectpw'] = 'Password is incorrect'
        

        return errors

####################################################################
    def edit_validator(self, postData):
        errors = {}
        # # validate field length requirements
        if len(postData['index_first_name']) == 0:
            errors['first_name_length'] = 'First name is required'
        if len(postData['index_last_name']) == 0:
            errors['last_name_length'] = 'Last name is required'
        if len(postData['index_email']) == 0:
            errors['email_length'] = 'Email is required'

        # #validate email pattern matches
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['index_email']):            
            errors['email_pattern'] = "Invalid email address!"

        # #validate email isn't already in the db
        email_match = User.objects.filter(email = postData['index_email'])
        if len(email_match) != 0:
            errors['email_exists_already'] = 'The email already exists. Please try a different name'

        return errors






####################################################################
class PostManager(models.Manager):
    def post_validator(self, postData):
        errors = {}

        #validate field length requirements are met
        if len(postData['quote_author']) < 3:
            errors['author_length'] = 'Author must be at least 3 characters. Please try again.'
        if len(postData['quote_quote']) < 10:
            errors['quote_length'] = 'Quote must be at least 3 characters. Please try again.'
        
        return errors










####################################################################


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    #posts_uploader
    #posts_liked

class Post(models.Model):
    author = models.CharField(max_length = 255)
    quote = models.TextField(null = True)
    poster = models.ForeignKey(User, related_name = 'posts_uploader', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name = 'posts_liked')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()