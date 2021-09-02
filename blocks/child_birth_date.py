
import localz
from .birth_date import BirthDate


class ChildBirthDate(BirthDate):
    request_message = localz.request_child_birth_date
    error_message = localz.incorrect_birth_date
    save_message = localz.child_birth_date_saved

