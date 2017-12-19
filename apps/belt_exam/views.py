# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):

    return render(request, 'belt_exam/index.html')

def show(request):
    try:
        request.session['user_id']
    except keyError:
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'registered_users': User.objects.all(),
    }

    return render(request, 'belt_exam/show.html', context)

def register(request):
    errors = User.objects.validate_registration(request.POST)
    if type(errors) == dict:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        request.session['user_id'] = errors.id
        messages.success(request, "Successfully registered!")
    return redirect('/show')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if type(errors) == dict:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        request.session['user_id'] = errors.id
        messages.success(request, "Successfully logged in!")
    return redirect('/show')

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')
