from django.db import models


class ClassDetails(models.Model):
    title = models.CharField(null=False, max_length=60)
    subtitle = models.CharField(null=False, max_length=60)

    def to_string(self):
        return ": ".join([self.title, self.subtitle])

    def __unicode__(self):
        return ": ".join([self.title, self.subtitle])


class Section(models.Model):
    parent_class = models.ForeignKey("ClassDetails")
    day_of_week = models.CharField(null=False, max_length=9)
    time_string = models.CharField(null=False, max_length=20)
    location = models.CharField(null=True, max_length=50)
    max_size = models.IntegerField(null=False)
    enrollment = models.IntegerField(null=False, default=0)

    def to_json(self):
        return {"day": self.day_of_week, "time": self.time_string,
                         "location": self.location, "max_size": self.max_size,
                         "enrollment": self.enrollment, "id": self.id,
                         "students": Student.objects.filter(current_section=self.id).values()}

    def reset_enrollment(self):
        self.enrollment = 0

    def add_student(self):
        self.enrollment += 1

    def delete_student(self):
        self.enrollment -= 1

    def __unicode__(self):
        return "/".join([self.day_of_week, self.time_string, self.location])


class Student(models.Model):

    full_name = models.CharField(null=False, max_length=100)
    email_address = models.CharField(null=False, max_length=100)
    current_section = models.ForeignKey("Section", null=True)
    parent_class = models.ForeignKey("ClassDetails", null=False)

    def set_section(self, day, time):
        try:
            new_section = Section.objects.get(day_of_week=day, time_string=time)
            self.current_section = new_section
        except Section.DoesNotExist:
            print "Could not identify section: %s \t %s. Aborting update to student's section" % (day, time)

    def get_section(self):
        return self.current_section

    def __unicode__(self):
        return self.full_name

    class Meta:
        unique_together = ("full_name", "parent_class")



#
# CUSTOM FORMS
# TODO: does not handle multiple choice fields right now
#
class CustomData(models.Model):
    
    full_name = models.CharField(verbose_name="Full name (first + last)", max_length=100)
    email = models.EmailField(verbose_name="Email Address", max_length=100)
    SID = models.IntegerField(verbose_name="Berkeley SID")
    affiliation = models.CharField(verbose_name="Department/Affiliation", max_length=100)
    full_time = models.BooleanField(verbose_name="Are you a full time student? (check this box if Yes)")
    dob = models.DateField(verbose_name="Date of birth (mm/dd/yyyy)")
    veteran = models.CharField(verbose_name='Are you a veteran or on active duty?', max_length=20)
    tbi = models.CharField(verbose_name='Have you ever experienced a concussion, a traumatic brain injury, or a stroke?',
                           max_length=20)
    adhd = models.CharField(verbose_name='Have you been diagnosed with Attention Deficit, ADHD, or LD?', max_length=40)
    meditation = models.CharField(verbose_name='Do you have experience meditating?', max_length=40)
    video_games = models.CharField(verbose_name='Do you have experience playing video games?', max_length=40)
    assessments = models.CharField(verbose_name='', max_length=40)
