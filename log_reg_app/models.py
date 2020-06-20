from django.db import models
from datetime import datetime
from datetime import date
import re

LETTERS_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if not LETTERS_REGEX.match(postData['first_name']):         
            errors['first_name_l'] = "First name must consist of letters only."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        if not LETTERS_REGEX.match(postData['last_name']):         
            errors['last_name_l'] = "Last name must consist of letters only."
        if postData['birthday'] =='':
            errors['birthday_b'] = "Birthday field can't be blank."
            return errors
        converted_date = datetime.strptime(postData['birthday'], '%Y-%m-%d').date()
        if converted_date >= date.today():
            errors['birthday_p'] = "Invalid Date (must be a past date)"
            return errors
        
        days_in_year = 365.2425
        age = int((date.today() - converted_date).days / days_in_year)
        if age < 13:
            errors['birthday'] = "You must be at least 13 years old"

        if len(postData['email']) < 1:
            errors['email'] = "Email field can't be blank."
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email_m'] = "Invalid email address!"
        result = User.objects.filter(email=postData['email'])
        if result:
            errors['email_f'] = 'Email address is already registered'
        if len(postData['pw']) < 8:
            errors['password'] = "Your password must be at least 8 characters."
        if postData['pw'] != postData['conf_pw']:
            errors['conf_password'] = "Your password and confirm password must match."
        return errors

    def profile_validator(self, postData, id):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if not LETTERS_REGEX.match(postData['first_name']):         
            errors['first_name_l'] = "First name must consist of letters only."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        if not LETTERS_REGEX.match(postData['last_name']):         
            errors['last_name_l'] = "Last name must consist of letters only."
        if len(postData['email']) < 1:
            errors['email'] = "Email field can't be blank."
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email_m'] = "Invalid email address!"
        user = User.objects.get(id=id)
        if user.email == postData['email']:
            return errors
        result = User.objects.filter(email=postData['email'])
        if result:
            errors['email_f'] = 'Email address is already registered'
        return errors
        

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    poster = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    poster = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

