
import re

import localz
from singleton import logger, api
from telebot.types import Message

from .answer_requestor import AnswerRequestor


class FirstName(AnswerRequestor):
    request_message = localz.request_first_name
    error_message = localz.incorrect_first_name
    save_message = localz.first_name_saved
    block_id = 'name'

    def _validate(self, message: Message):
        message_text = message.text
        #bool(re.match('^[а-яА-Яa-zA-ZіІїЇєЄҐґ-]{2,}$', message_text))
        if (message_text is None
                or not bool(re.match('^.{2,}$', message_text))):
            return False

        return True

    def process_message(self, message: Message):
        if super().process_message(message):
            return

        if not self._validate(message):
            logger.debug(self.error_message)
            api().reply_to(message, self.error_message, reply_markup = self.remove_markup)
            api().reply_to(message, self.request_message, reply_markup = self.add_markup)
            return

        api().reply_to(message, self.save_message, reply_markup = self.remove_markup)
        self.finish({self.block_id: message.text})
