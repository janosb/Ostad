from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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


# TODO: remove after testing
@login_required()
def generate_mock_data(request):
    from sections.models import *

    ClassDetails.objects.all().delete()
    classes = [
        {"title": "Tamarkoz", "subtitle": "Sufi Meditation"},
        {"title": "Cognitive Training", "subtitle": "Attention Training"},
        {"title": "Python", "subtitle": "For Beginners"}
    ]
    sections = [
        {"day_of_week": "Monday", "t_start": "12:00pm", "t_end": "1:30pm", "location": "25 Wheeler", "nmax": 25},
        {"day_of_week": "Tuesday", "t_start": "1:00pm", "t_end": "3:30pm", "location": "5181 Tolman", "nmax": 25},
        {"day_of_week": "Thursday", "t_start": "2:00pm", "t_end": "4:30pm", "location": "Sproul Plaza", "nmax": 25},
        {"day_of_week": "Friday", "t_start": "3:00pm", "t_end": "4:30pm", "location": "Telegraph Blondies Pizza", "nmax": 45},
        {"day_of_week": "Saturday", "t_start": "6:00pm", "t_end": "9:30pm", "location": "Euclid Apartments", "nmax": 10}
    ]
    students = [
        {"name": "Mock User 1", "email": "user1@berkeley.edu"},
        {"name": "Fake User 2", "email": "faker2@berkeley.edu"},
        {"name": "False User 3", "email": "false3@berkeley.edu"},
        {"name": "Persian Burger", "email": "bongo@burger.com"},
        {"name": "La Mission", "email": "burrita@euclid.org"}
    ]

    for class_instance in classes:
        this_class, created = ClassDetails.objects.get_or_create(title=class_instance["title"], subtitle=class_instance["subtitle"])
        for (section, student) in zip(sections, students):
            this_section, created = Section.objects.get_or_create(parent_class=this_class, day_of_week=section["day_of_week"],
                                                         time_string="%s-%s" % (section["t_start"], section["t_end"]),
                                                         location=section["location"], max_size=section["nmax"]
                                                         )
            this_student, created = Student.objects.get_or_create(parent_class=this_class, current_section=this_section,
                                                            full_name=student["name"], email_address=student["email"])
            this_section.add_student()
            this_section.save()

    return HttpResponseRedirect("/")

