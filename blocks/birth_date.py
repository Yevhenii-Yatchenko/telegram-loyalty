import re

import localz
from telebot.types import Message

from .first_name import FirstName


class BirthDate(FirstName):
    request_message = localz.request_birth_date
    error_message = localz.incorrect_birth_date
    save_message = localz.birth_date_saved
    block_id = 'date_birth'

    def _validate(self, message: Message):
        message_text = message.text
        if (message_text is None
                or not bool(re.match('^(?:0[1-9]|[12][0-9]|3[01])[-/.](?:0[1-9]|1[012])[-/.](?:19\d{2}|20[01][0-9]|2020|2021)$', message_text))):
            return False

        return True
