from django import forms
from captcha.fields import CaptchaField
import inspect

time_choices = ["12:00pm", "12:30pm", "1:00pm", "1:30pm", "2:00pm", "2:30pm", "3:00pm", "3:30pm", "4:00pm",
                "4:30pm", "5:00pm", "5:30pm", "6:00pm", "6:30pm", "7:00pm", "7:30pm", "8:00pm", "8:30pm",
                "9:00pm", "9:30pm", "10:00pm"]

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def gen_start_time_choices():
    for time in time_choices:
        yield (time, time)

def gen_end_time_choices():
    for time in time_choices:
        yield (time, time)

def gen_days_choices():
    for day in days_of_week:
        yield (day, day)


class ClassForm(forms.Form):
    title = forms.CharField(label='Class Name', required=True)
    subtitle = forms.CharField(label='Subtitle', required=True)

class SectionForm(forms.Form):
    #parent_class = forms.HiddenInput(label='class_id', required=True)
    day_of_week = forms.ChoiceField(label='Day of week', choices=gen_days_choices(), required=True)
    t_start = forms.ChoiceField(label='Start time', choices=gen_start_time_choices(), required=True)
    t_end = forms.ChoiceField(label='End time', choices=gen_end_time_choices())
    location = forms.CharField(label='Location', max_length=100)
    max_size = forms.IntegerField(label='Maximum number of students', required=True)


class StudentForm(forms.Form):
    full_name = forms.CharField(label="Full name (first + last)", max_length=100, required=True)
    email = forms.EmailField(label="Preferred Email Address", max_length=100, required=True)
    captcha = CaptchaField()


#
# CUSTOM FORMS
# TODO: does not handle multiple choice fields right now
#
class CustomForm(forms.Form):
    full_name = forms.CharField(label="Full name (first + last)", max_length=100, required=True)
    email = forms.EmailField(label="Email Address", max_length=100, required=True)
    SID = forms.IntegerField(label="Berkeley SID", required=True)
    affiliation = forms.CharField(label="Department/Affiliation", max_length=100, required=True)
    full_time = forms.BooleanField(label="Are you a full time student? (check this box if Yes) ", required=False)
    dob = forms.DateField(label="Date of birth (mm/dd/yyyy)", widget=forms.widgets.DateInput(format="%m/%d/%Y"), required=True)
    veteran = forms.ChoiceField(label='Are you a veteran or on active duty?', widget=forms.RadioSelect,
                                choices=(("none", "Neither"), ("vet", "Veteran"), ("active", "Active Duty")),
                                required=True)
    tbi = forms.MultipleChoiceField(label='Have you ever experienced a concussion, a traumatic brain injury, or a stroke?',
                                    choices=(("conc", "Concussion"), ("tbi", "TBI"),
                                             ("stroke", "Stroke"), ("none", "None")),
                                    widget=forms.CheckboxSelectMultiple,
                                    required=True)
    adhd = forms.MultipleChoiceField(label='Have you been diagnosed with Attention Deficit, ADHD, or LD?',
                                     choices=(("add", "Attention Deficit Disorder"),
                                              ("adhd", "Attention Deficit Hyperactivity Disorder"), ("none", "None"),
                                              ("other", "Other")),
                                     widget=forms.CheckboxSelectMultiple, required=True)
    meditation = forms.ChoiceField(label='Do you have experience meditating?',
                                   choices=(("10", "Yes, I meditate 10 or more hours a week"),
                                            ("5", "Yes, I meditate 5 or so hours a week"),
                                            ("1-2", "Yes, I meditate 1-2 hours a week"),
                                            ("little", "A little, but I don't really meditate regularly"),
                                            ("none", "No, I don't have much meditation experience"),
                                            ("other", "Other")), widget=forms.RadioSelect, required=True)
    video_games = forms.ChoiceField(label='Do you have experience playing video games?',
                                    choices=(("10", "Yes, I play 10 or more hours a week"),
                                             ("5", "Yes, I play 5 or so hours a week"),
                                             ("1-2", "Yes, I play 1-2 hours a week"),
                                             ("little", "A little, but I don't really play regularly"),
                                             ("none", "No, I don't have much gaming experience"),
                                             ("other", "Other")), required=True, widget=forms.RadioSelect)
    assessments = forms.ChoiceField(label='Are you comfortable and excited to participate in the cognitive and neural assessments?',
                                    choices=(("yes_all", "Yes, I'm excited and up for all the assessments"),
                                             ("yes_notsure", "Yes, but I'm not sure about some of them"),
                                             ("no", "No, I'm not comfortable participating in any measurements"),
                                             ("other", "Other")), widget=forms.RadioSelect,
                                    help_text="These could include measures of memory capacity and attention, " +
                                              "as well as brain imaging like fMRI or EEG (taking images of your brain " +
                                              "at rest and measuring brain wave activity).", required=True)
    why_take_class = forms.CharField(label="Why do you want to take this class?", widget=forms.Textarea,
                                     help_text="Feel free to mention any personal goals you'd like to reach, interests in the materials you have, etc.")
    sections = forms.MultipleChoiceField(label="Below are the section signups. " +
                                               "You can answer check as many options as you like to increase your chances of finding space.",
                                         choices=((1, "Tuesdays 11:00AM - 12:30PM"), (2, "Tuesdays 2:00PM - 3:30PM"),
                                                  (3, "Tuesdays 3:30PM - 5:00PM"), (4, "Thursdays 2:00PM - 3:30PM"),
                                                  (5, "Thursdays 6:00PM - 7:30PM"), (6, "Thursdays 7:30PM - 9:00PM"),),
                                         widget=forms.CheckboxSelectMultiple, required=True)

    def get_fields(self):
        for tup in inspect.getmembers(self):
            if tup[0] == "fields":
                return tup[1]

