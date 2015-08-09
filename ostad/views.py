from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from sections.helpers import get_all_classes

def home(request):
    return HttpResponseRedirect('/sections')

def home_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/sections')
    return render(request, 'login.html', {'classes': get_all_classes()})


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/sections')
    return HttpResponseRedirect('/')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

