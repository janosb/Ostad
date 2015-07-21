from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from models import Section, Student
from .forms import SectionForm

import json


def new_section(day, start_time, end_time, location=None):
    time_str = "%s-%s" % (start_time, end_time)
    section, created = Section.objects.get_or_create(day_of_week=day, time_string=time_str)
    if created:
        print "successfully created section on %s at time %s" % (day, time_str)
        if location:
            print "updating location to %s" % location
            section.location = location
    else:
        print "section already exists on %s at %s" % (day, time_str)
        if location:
            print "updating location to %s" % location
            section.location = location
    section.save()


def list_sections(request):
    all_sections = Section.objects.all()
    out_json = []
    for section in all_sections:
        out_json.append({"day": section.day_of_week, "time": section.time_string, "location": section.location})
    form = SectionForm()
    return render(request, 'new_section.html', {'form': form, 'current_list': json.dumps(out_json)})


def add_section(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #new_section(form.day_of_week, form.t_start, form.t_end)
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SectionForm()

    return render(request, 'new_section.html', {'form': form, 'current_list': ''})

def save_section(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_section(request.POST.get('day_of_week'), request.POST.get('t_start'),
                        request.POST.get('t_end'), location=request.POST.get('location', None))
            return HttpResponseRedirect('/sections')
    else:
        return HttpResponseRedirect('/sections/add')


# TODO: REMOVE THIS AFTER TESTING
def remove_sections(request):
    Section.objects.all().delete();
    return HttpResponseRedirect('/sections')
