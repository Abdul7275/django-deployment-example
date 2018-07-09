# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from basicapp.forms import UserForm,UserProfileInfoForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    return render(request,"basicapp/index.html")


@login_required
def special(request):
    return HttpResponse("You are loggedin Hurray..!")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



#User registration view
def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) #hashing of password is done here
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user   #used for OneToOne mapping with User Model

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print (user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,"basicapp/registration.html",{'user_form':user_form,'profile_form':profile_form,'registered':registered})



def user_login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("User not active")
        else:
            print ("Someone tried to access and failed")
            print ("Username: {} and Password: {}".format(username,password))
            return HttpResponse("Invalid login details are supplied")
    else:
        return render(request,'basicapp/login.html',{})
