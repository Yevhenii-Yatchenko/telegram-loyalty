
from typing import Dict
import localz
from telebot.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

from .answer_requestor import AnswerRequestor
from singleton import logger, api

reply_markup = ReplyKeyboardMarkup()
yes = KeyboardButton(localz.yes)
no = KeyboardButton(localz.no)
reply_markup.add(yes, no)

remove_markup = ReplyKeyboardRemove(selective=False)

model_yes = 'yes'
model_no = 'no'


class AskIfChildren(AnswerRequestor):
    request_message = localz.request_children
    error_message = localz.incorrect_yes_no
    add_markup = reply_markup
    remove_markup = remove_markup
    block_id = 'ask_if_children'

    __localz_model_map = {
        localz.yes: model_yes,
        localz.no: model_no,
    }

    def _validate(self, message: Message):
        message_text = message.text
        if (message_text is None or message_text not in (localz.yes, localz.no)):
            return False

        message.text = self.__localz_model_map[message_text]

        return True

    def process_message(self, message: Message):
        if super().process_message(message):
            return

        if not self._validate(message):
            logger.debug(self.error_message)
            api().reply_to(message, self.error_message, reply_markup = self.remove_markup)
            api().reply_to(message, self.request_message, reply_markup = self.add_markup)
            return

        if message.text == model_no:
            api().reply_to(message, localz.children_not_saved,
                           reply_markup = self.remove_markup)
            self.finish({self.block_id: model_no})
            return

        api().reply_to(message, localz.start_children_data_collection, reply_markup = self.remove_markup)
        self.finish({self.block_id: model_yes})