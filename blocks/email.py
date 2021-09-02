
import re

import localz
from telebot.types import Message

from .first_name import FirstName


class Email(FirstName):
    request_message = localz.request_email
    error_message = localz.incorrect_email
    save_message = localz.email_saved
    block_id = 'email'

    def _validate(self, message: Message):
        message_text = message.text
        if (message_text is None
                or not bool(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message_text))):
            return False

        return True
