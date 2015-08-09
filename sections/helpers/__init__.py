from sections.models import ClassDetails

class AddStatus():

    FULL_SECTION = 0
    NON_EXISTENT_CLASS = 1
    NON_EXISTENT_SECTION = 2
    STUDENT_ALREADY_EXISTS = 3
    INVALID_EMAIL = 4
    SUCCESS = 5


def get_all_classes():
    all_classes = ClassDetails.objects.all()
    return all_classes.values()