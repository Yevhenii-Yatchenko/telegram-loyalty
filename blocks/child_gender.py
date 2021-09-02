
import localz
from .gender import Gender
from telebot.types import (KeyboardButton, Message, ReplyKeyboardMarkup)


reply_markup = ReplyKeyboardMarkup()
male = KeyboardButton(localz.boy)
female = KeyboardButton(localz.girl)
reply_markup.add(male, female)

model_male = 'M'
model_female = 'F'


class ChildGender(Gender):
    request_message = localz.request_child_gender
    error_message = localz.incorrect_gender
    save_message = localz.child_gender_saved
    add_markup = reply_markup

    __localz_model_map = {
        localz.boy: model_male,
        localz.girl: model_female,
    }

    def _validate(self, message: Message):
        message_text = message.text
        if (message_text is None
                or message_text not in (localz.boy, localz.girl)):
            return False

        message.text = self.__localz_model_map[message_text]

        return True