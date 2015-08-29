from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from models import Section, Student, ClassDetails, CustomData
from .forms import SectionForm, StudentForm, CustomForm, ClassForm
from .helpers import AddStatus, get_all_classes
from ostad import settings


def show_classes(request):
    form = ClassForm()
    return render(request, 'classes.html', {"classes": get_all_classes(), 'is_admin': request.user.is_authenticated(),
                                            "form": form})

def new_section(class_id, day, start_time, end_time, max_size=25, location=None):
    time_str = "%s-%s" % (start_time, end_time)
    class_instance = ClassDetails.objects.get(id=class_id)
    section, created = Section.objects.get_or_create(parent_class=class_instance, day_of_week=day, time_string=time_str,
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


def list_sections(request, class_id):
    all_sections = Section.objects.filter(parent_class=class_id).order_by('id')
    json_list = []
    for section in all_sections:
        json_list.append(section.to_json())
    form = SectionForm()

    class_details = ClassDetails.objects.get(id=class_id)
    return render(request, 'list_sections.html', {'form': form, 'current_list': json_list,
                                                  'class_details': class_details,
                                                  'classes': get_all_classes(),
                                                  'is_admin': request.user.is_authenticated()})


def add_section(request, class_id):
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

    class_details = ClassDetails.objects.get(id=class_id)
    return render(request, 'new_section.html', {'form': form, 'current_list': '', 'class_details': class_details,
                                                'classes': get_all_classes(), 'is_admin': request.user.is_authenticated()})


def save_section(request, class_id):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            new_section(class_id, data.get("day_of_week"), data.get("t_start"), data.get("t_end"), location=data.get("location"),
                        max_size=data.get("max_size"))
            return HttpResponseRedirect('/sections/%s' % class_id)
    else:
        return HttpResponseRedirect('/sections/add')


# TODO: REMOVE THIS AFTER TESTING
@login_required()
def remove_sections(request, class_id, section_id):
    if settings.DEBUG:
        if class_id and section_id:
            class_instance = ClassDetails.objects.get(id=class_id)
            Section.objects.get(parent_class=class_instance, id=section_id).delete()
            return HttpResponseRedirect('/sections/%s' % class_id)
        elif class_id and not section_id:
            class_instance = ClassDetails.objects.get(id=class_id)
            Section.objects.filter(parent_class=class_instance).delete()
        else:
            Section.objects.all().delete()
    return HttpResponseRedirect('/sections')


def new_student(full_name, email, class_id, section_id):
    try:
        class_instance = ClassDetails.objects.get(id=class_id)
        section = Section.objects.get(id=section_id)
        if section.get_enrollment() >= section.max_size:
            print "cannot add to full section %d" % section_id
            return AddStatus.FULL_SECTION
    except Section.DoesNotExist:
        print "invalid section id %d" % section_id
        return AddStatus.NON_EXISTENT_SECTION
    except ClassDetails.DoesNotExist:
        print "invalid class id %d" % class_id
        return AddStatus.NON_EXISTENT_CLASS

    # check for full name in db
    try:
        Student.objects.get(full_name=full_name, parent_class=class_instance)
    except Student.DoesNotExist:
        # expected behavior
        pass

    # check for email in db
    try:
        Student.objects.get(email_address=email, parent_class=class_instance)
        return AddStatus.STUDENT_ALREADY_EXISTS
    except Student.DoesNotExist:
        # expected behavior
        pass

    student, created = Student.objects.get_or_create(full_name=full_name, parent_class=class_instance)
    if not created:
        return AddStatus.STUDENT_ALREADY_EXISTS
    else:
        student.email_address = email
        student.current_section = section
        student.save()
        return AddStatus.SUCCESS


def add_student(request, class_id, section_id):
    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        print "Tried to get unregistered section %d" % section_id
        return HttpResponseRedirect('/sections')
    form = StudentForm()

    class_details = ClassDetails.objects.get(id=class_id)
    return render(request, 'new_student.html', {'form': form, 'section_info': section.to_json(),
                                                'class_details': class_details, 'classes': get_all_classes(),
                                                'is_admin': request.user.is_authenticated()})


def save_student(request, class_id):
    class_instance = ClassDetails.objects.get(id=class_id)
    email_subject = '%s: Confirmation of enrollment' % class_instance.title
    email_disclaimer = "\n\nIf you believe this to be erroneous, please contact the me at %s" \
                       % class_instance.admin_email + "\n\nSincerely, \n%s" % class_instance.admin_name
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST)
        section_id = int(request.POST.get('section_id'))
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            add_status = new_student(data.get("full_name"), data.get("email"), class_id, section_id)
            if add_status == AddStatus.SUCCESS:
                section = Section.objects.get(id=section_id)
                message = "We have added you to the section on %s %s in %s. Current enrollment is %d / %d." \
                          % (section.day_of_week, section.time_string, section.location,
                             section.get_enrollment(), section.max_size)

                email_message = ("Dear %s,\n\n" % data.get("full_name")) + message + email_disclaimer
                EmailMessage(email_subject, email_message, to=[data.get("email")]).send()

                return render(request, 'add_result.html', {'title': 'Success!', 'message': message,
                                                'class_details': class_instance,
                                                'classes': get_all_classes()})
            else:
                student = None
                if add_status == AddStatus.FULL_SECTION:
                    title = 'Hmmm...'
                    message = "Sorry, that section is already full! Please register for another."
                elif add_status == AddStatus.NON_EXISTENT_CLASS:
                    title = 'Hmmm...'
                    message = "Sorry, that class does not exist! Please register for another."
                elif add_status == AddStatus.NON_EXISTENT_SECTION:
                    title = 'Hmmm...'
                    message = "Sorry, that section does not exist! Please register for another."
                elif add_status == AddStatus.STUDENT_ALREADY_EXISTS:
                    student = Student.objects.filter(full_name=data.get("full_name"))
                    if len(student) != 1:
                        student = Student.objects.filter(email_address=data.get("email"))
                    student = student.first()
                    previous_section = student.current_section
                    previous_class_id = previous_section.parent_class.id
                    if previous_section.id == section_id:
                        title = 'Already registered'
                        message = "We found you in our database already. Please check your status below. See you in class!"
                    else:
                        newer_section = Section.objects.get(id=section_id)
                        student.current_section = newer_section
                        student.save()

                        title = "Switched Sections"
                        message = "You have successfully switched sections to the class on %s %s in %s. Current enrollment is %d / %d. See you in class!" \
                          % (newer_section.day_of_week, newer_section.time_string, newer_section.location,
                             newer_section.get_enrollment(), newer_section.max_size)
                        email_message = ("Dear %s,\n\n" % data.get("full_name")) + message + email_disclaimer
                        EmailMessage(email_subject, email_message, to=[data.get("email")]).send()
                return render(request, 'add_result.html', {'title': title, 'message': message, 'user_info': student,
                                                           'classes': get_all_classes(), 'class_details': class_instance,
                                                           'is_admin': request.user.is_authenticated()})

        else:
            section = Section.objects.get(id=section_id)
            return render(request, 'new_student.html', {'form': form, 'section_info': section.to_json(),
                                                        'class_details': class_instance, 'classes': get_all_classes(),
                                                        'is_admin': request.user.is_authenticated()})
    else:
        return HttpResponseRedirect('/sections')


@login_required()
def remove_students(request, class_id, student_id):
    if not student_id and settings.DEBUG:
        Student.objects.filter(parent_class_id=class_id).delete()
    else:
        try:
            Student.objects.get(id=student_id, parent_class_id=class_id).delete()
        except Student.DoesNotExist:
            print "Invalid class id %s or student id %s" % (class_id, student_id)
    return HttpResponseRedirect('/sections/%s' % class_id)


def save_class(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ClassForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            class_instance, created = ClassDetails.objects.get_or_create(title=data.get("title"), subtitle=data.get("subtitle"))
            if not created:
                return render(request, 'classes.html',
                              {"classes": get_all_classes(), 'is_admin': request.user.is_authenticated(),
                               "form": form, "error_message": "Class already exists"})
            return HttpResponseRedirect('/sections/%d' % class_instance.id)
    return HttpResponseRedirect('sections')


# TODO: REMOVE THIS AFTER TESTING
@login_required()
def remove_classes(request):
    if settings.DEBUG:
        ClassDetails.objects.all().delete()
    return HttpResponseRedirect('/sections')

#
# CUSTOM FORMS
# TODO: does not handle multiple choice fields right now
#
def custom_signup_form(request):
    # TODO: get class id from somewhere
    class_details = ClassDetails.objects.first()
    form = CustomForm()
    return render(request, 'custom_form.html', {'form': form, 'class_details': class_details})


def custom_form_save(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CustomForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_custom_form_entry(form)
        else:
            message = 'Form was not valid...'
            # TODO: get class id from somewhere
            class_details = ClassDetails.objects.first()
            return render(request, 'custom_form.html', {'form': form, 'class_details': class_details,
                                                        'error_message': message})
    return HttpResponse("Thanks!")


def new_custom_form_entry(form):
    fields = form.get_fields()
    data = form.cleaned_data
    record = CustomData()
    for field in fields:
        setattr(record, field, data.get(field))
    record.save()
