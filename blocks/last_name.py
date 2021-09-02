
import localz
from .first_name import FirstName


class LastName(FirstName):
    request_message = localz.request_last_name
    error_message = localz.incorrect_last_name
    save_message = localz.last_name_saved
    block_id = 'surname'