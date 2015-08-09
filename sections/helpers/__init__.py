from sections.models import ClassDetails

class AddStatus():

    FULL_SECTION = 0
    NON_EXISTENT_SECTION = 1
    STUDENT_ALREADY_EXISTS = 2
    INVALID_EMAIL = 3
    SUCCESS = 4


def get_all_classes():
    all_classes = ClassDetails.objects.all()
    return all_classes.values()