
import localz
from telebot.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

from .first_name import FirstName

reply_markup = ReplyKeyboardMarkup()
male = KeyboardButton(localz.yes)
female = KeyboardButton(localz.no)
reply_markup.add(male, female)

remove_markup = ReplyKeyboardRemove(selective=False)

model_yes = 'yes'
model_no = 'no'


class Agreement(FirstName):
    request_message = localz.request_agreement
    error_message = localz.incorrect_agreement
    save_message = localz.agreement_saved
    add_markup = reply_markup
    remove_markup = remove_markup
    block_id = 'agreement'

    __localz_model_map = {
        localz.yes: model_yes,
        localz.no: model_no,
    }

    def _validate(self, message: Message):
        message_text = message.text
        if (message_text is None or message_text != localz.yes):
            return False

        message.text = self.__localz_model_map[message_text]

        return True
