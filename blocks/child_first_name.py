
import localz
from .first_name import FirstName


class ChildFirstName(FirstName):
    request_message = localz.request_child_first_name
    error_message = localz.incorrect_first_name
    save_message = localz.child_first_name_saved
