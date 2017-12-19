# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z\s]+$')

# Create your models here.
class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = {}
        if len(self.filter(email=post_data['email'])) > 0:
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['loginError'] = "Email or password is incorrect"
        else:
            errors['loginError2'] = "Email or password is incorrect"
        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = {}
        if len(post_data['email']) <= 0:
            errors['email'] = "Email field is required."
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors['emailVal'] = "Invalid email dork!.."
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['existing_email'] = "Email is already in use."
        if len(post_data['fname']) < 2:
            errors['fname'] = "First name field must contain at least 2 characters."
        if len(post_data['lname']) < 2:
            errors['lname'] = "Last name field must contain at least 2 characters."
        if not re.match(NAME_REGEX, post_data['fname']):
            errors['fnameChar'] = "First Name field must contain letters only."
        if not re.match(NAME_REGEX, post_data['lname']):
            errors['lnameChar'] = "Last name field must contain letters only."
        if len(post_data['password']) == 0:
            errors['password'] = "Password field is required."
        if len(post_data['password']) < 8:
            errors['passwordLength'] = "Must contain 8 characters or more."
        if post_data['password'] != post_data['pwd_conf']:
            errors['pwd_conf'] = "Password must match!"

        if not errors:
            hashedpwd = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt(6))
            new_user = self.create(
                email = post_data['email'],
                first_name = post_data['fname'],
                last_name = post_data['lname'],
                address = post_data['address'],
                credit_card = post_data['credit'],
                password = hashedpwd,
            )
            return new_user
        return errors

class User(models.Model):
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    credit_card = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return "{} {} {} {} {}".format(self.email, self.first_name, self.last_name, self.address, self.credit_card)
