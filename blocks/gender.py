import re

import localz
from telebot.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

from .first_name import FirstName

reply_markup = ReplyKeyboardMarkup()
male = KeyboardButton(localz.male)
female = KeyboardButton(localz.female)
reply_markup.add(male, female)

remove_markup = ReplyKeyboardRemove(selective=False)

model_male = 'M'
model_female = 'F'


class Gender(FirstName):
    request_message = localz.request_gender
    error_message = localz.incorrect_gender
    save_message = localz.gender_saved
    add_markup = reply_markup
    remove_markup = remove_markup
    block_id = 'gender'

    __localz_model_map = {
        localz.male: model_male,
        localz.female: model_female,
    }

    def _validate(self, message: Message):
        message_text = message.text
        if (message_text is None
                or message_text not in (localz.male, localz.female)):
            return False

        message.text = self.__localz_model_map[message_text]

        return True
