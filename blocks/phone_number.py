
import re

import localz
import rest_client
from singleton import logger, api
from telebot.types import Message

from .answer_requestor import AnswerRequestor


class PhoneNumber(AnswerRequestor):
    #request_message = localz.request_phone_number
    error_message = localz.rerequest_phone_number
    save_message = localz.phone_number_saved
    block_id = 'phone'

    def __parse_number(self, message: Message) -> str:
        message_text = message.text
        if message_text is not None:
            message_text = re.sub(r'[^\d]', '', message_text)
            if message_text.startswith('0'):
                message_text = '38' + message_text
            if message_text.startswith('8'):
                message_text = '3' + message_text

        return message_text

    def __request_phone_number(self, message: Message):
        api().reply_to(message, localz.rerequest_phone_number)

    def _validate(self, message: Message):
        message_text = self.__parse_number(message)
        if (message.content_type != 'text' or not message_text.isdigit()):
            return False

        return True

    def process_message(self, message: Message):
        if super().process_message(message):
            return

        if message.text == '/start':
            api().reply_to(message, localz.request_phone_number)
            return

        if not self._validate(message):
            error_message = localz.incorrect_number
            logger.debug(error_message)
            api().reply_to(message, error_message)
            self.__request_phone_number(message)
            return

        self.__check_number_status(message)

    def __check_number_status(self, message: Message):
        message_text = self.__parse_number(message)
        data = rest_client.get_number_status(message_text)

        errors = data.get('errors')
        card_id = data.get('cardid')

        if errors is None and card_id is not None:
            api().reply_to(message, localz.phone_number_saved)
            self.finish({
                self.block_id: int(message_text),
                'cardid': card_id
            })
            return

        try:
            error_code = errors[0]['code']

            if error_code == 31:
                localized_message = localz.not_found_number
            elif error_code == 32:
                bonuses = error_code = errors[0].get('bonuses')
                if bonuses is not None:
                    localized_message = localz.already_active_number_with_bonuses.format(bonuses)
                else:
                    localized_message = localz.already_active_number
            else:
                localized_message = localz.internal_server_error
        except (TypeError, IndexError, KeyError):
            localized_message = localz.internal_server_error

        api().reply_to(message, localized_message)
        self.__request_phone_number(message)
