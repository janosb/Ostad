from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from models import Section, Student
from .forms import SectionForm, StudentForm
from .helpers import AddStatus


def new_section(day, start_time, end_time, max_size=25, location=None):
    time_str = "%s-%s" % (start_time, end_time)
    section, created = Section.objects.get_or_create(day_of_week=day, time_string=time_str,
                                                     location=location, max_size=max_size)
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
    section.max_size = max_size
    section.save()


def update_enrollment_after_switch(previous_section, newer_section):
    previous_section.delete_student()
    previous_section.save()
    newer_section.add_student()
    newer_section.save()


def list_sections(request):
    all_sections = Section.objects.all()
    json_list = []
    for section in all_sections:
        json_list.append(section.to_json())
    form = SectionForm()
    return render(request, 'new_section.html', {'form': form, 'current_list': json_list})


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
                        request.POST.get('t_end'), location=request.POST.get('location', None),
                        max_size=request.POST.get('max_size'))
            return HttpResponseRedirect('/sections')
    else:
        return HttpResponseRedirect('/sections/add')

# TODO: REMOVE THIS AFTER TESTING
def remove_sections(request):
    Section.objects.all().delete()
    return HttpResponseRedirect('/sections')




def new_student(full_name, email, section_id):
    try:
        section = Section.objects.get(id=section_id)
        if section.enrollment >= section.max_size:
            print "cannot add to full section %d" % section_id
            return AddStatus.FULL_SECTION
    except Section.DoesNotExist:
        print "invalid section id %d" % section_id
        return AddStatus.NON_EXISTENT_SECTION

    # check for full name in db
    try:
        student = Student.objects.get(full_name=full_name)
        return AddStatus.STUDENT_ALREADY_EXISTS
    except Student.DoesNotExist:
        # expected behavior
        pass

    # check for email in db
    try:
        student = Student.objects.get(email_address=email)
        return AddStatus.STUDENT_ALREADY_EXISTS
    except Student.DoesNotExist:
        # expected behavior
        pass

    if "berkeley.edu" not in email:
        return AddStatus.INVALID_EMAIL

    student, created = Student.objects.get_or_create(full_name=full_name, email_address=email, current_section=section)
    if not created:
        return AddStatus.STUDENT_ALREADY_EXISTS
    student.save()
    return AddStatus.SUCCESS

def add_student(request, section_id):
    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        print "Tried to get unregistered section %d" % section_id
        return HttpResponseRedirect('/sections')
    form = StudentForm()
    return render(request, 'new_student.html', {'form': form, 'section_info': section.to_json()})

def save_student(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            add_status = new_student(request.POST.get('full_name'), request.POST.get('email'),
                        request.POST.get('section_id'))
            if add_status == AddStatus.SUCCESS:
                section = Section.objects.get(id=request.POST.get('section_id'))
                section.enrollment += 1
                section.save()
                message = "We have added you to the section on %s %s in %s. Current enrollement is %d / %d." \
                          % (section.day_of_week, section.time_string, section.location,
                             section.enrollment, section.max_size)
                return render(request, 'add_result.html', {'title': 'Success!', 'message': message})
            else:
                student = None
                if add_status == AddStatus.FULL_SECTION:
                    title = 'Hmmm...'
                    message = "Sorry, that section is already full! Please register for another."
                elif add_status == AddStatus.NON_EXISTENT_SECTION:
                    title = 'Hmmm...'
                    message = "Sorry, that section does not exist! Please register for another."
                elif add_status == AddStatus.INVALID_EMAIL:
                    title = 'Hmmm...'
                    message = "Invalid email. Please provide your university-issued (berkeley.edu) email address."
                elif add_status == AddStatus.STUDENT_ALREADY_EXISTS:
                    student = Student.objects.filter(full_name=request.POST.get('full_name'))
                    if len(student) != 1:
                        student = Student.objects.filter(email_address=request.POST.get('email'))
                    student = student.first()
                    previous_section = student.current_section
                    if previous_section.id == int(request.POST.get('section_id')):
                        title = 'Already registered'
                        message = "We found you in our database already. Please check your status below. See you in class!"
                    else:
                        newer_section = Section.objects.get(id=request.POST.get('section_id'))
                        student.current_section = newer_section
                        student.save()
                        #update enrollment numbers
                        update_enrollment_after_switch(previous_section, newer_section)

                        title = "Switched Sections"
                        message = "You have successfully switched sections. Please check your status below. See you in class!"
                return render(request, 'add_result.html', {'title': title, 'message': message, 'user_info': student})

        else:
            return HttpResponse(str(form))
    else:
        return HttpResponseRedirect('/sections')


# TODO: REMOVE THIS AFTER TESTING
def remove_students(request):
    Student.objects.all().delete()
    for section in Section.objects.all():
        section.reset_enrollment()
        section.save()
    return HttpResponseRedirect('/sections')
