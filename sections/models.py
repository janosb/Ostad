from django.db import models


class Section(models.Model):

    day_of_week = models.CharField(null=False, max_length=9)
    time_string = models.CharField(null=False, max_length=20)
    location = models.CharField(null=True, max_length=50)


class Student(models.Model):

    full_name = models.CharField(null=False, max_length=100)
    email_address = models.CharField(null=False, max_length=100)
    current_section = models.OneToOneField("Section")

    def set_section(self, day, time):
        try:
            new_section = Section.objects.get(day_of_week=day, time_string=time)
            self.current_section = new_section
        except:
            print "Could not identify section: %s \t %s. Aborting update to student's section" % (day, time)

    def get_section(self):
        return self.current_section
