from django.db import models


class Section(models.Model):

    day_of_week = models.CharField(null=False, max_length=9)
    time_string = models.CharField(null=False, max_length=20)
    location = models.CharField(null=True, max_length=50)
    max_size = models.IntegerField(null=False)
    enrollment = models.IntegerField(null=False, default=0)

    def to_json(self):
        return {"day": self.day_of_week, "time": self.time_string,
                         "location": self.location, "max_size": self.max_size,
                         "enrollment": self.enrollment, "id": self.id}

    def reset_enrollment(self):
        self.enrollment = 0

    def add_student(self):
        self.enrollment += 1

    def delete_student(self):
        self.enrollment -= 1

class Student(models.Model):

    full_name = models.CharField(null=False, max_length=100)
    email_address = models.CharField(null=False, max_length=100)
    current_section = models.ForeignKey("Section")

    def set_section(self, day, time):
        try:
            new_section = Section.objects.get(day_of_week=day, time_string=time)
            self.current_section = new_section
        except Section.DoesNotExist:
            print "Could not identify section: %s \t %s. Aborting update to student's section" % (day, time)

    def get_section(self):
        return self.current_section
