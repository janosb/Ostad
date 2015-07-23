from django import forms

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


class SectionForm(forms.Form):
    day_of_week = forms.ChoiceField(label='Day of week', choices=gen_days_choices(), required=True)
    t_start = forms.ChoiceField(label='Start time', choices=gen_start_time_choices(), required=True)
    t_end = forms.ChoiceField(label='End time', choices=gen_end_time_choices())
    location = forms.CharField(label='Location', max_length=100)
    max_size = forms.IntegerField(label='Maximum number of students', required=True)


class StudentForm(forms.Form):
    full_name = forms.CharField(label="Full name (first + last)", max_length=100)
    email = forms.EmailField(label="Berkeley Email Address", max_length=100)
