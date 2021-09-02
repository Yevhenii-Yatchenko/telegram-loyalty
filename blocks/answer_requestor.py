from typing import Dict

from .base import Block
from singleton import api


class AnswerRequestor(Block):
    request_message = None
    add_markup = None
    remove_markup = None

    block_id = 'answer_requestor'

    def __init__(self, user_id, callback):
        super().__init__(user_id, callback)

        if self.request_message is not None and not self.data.data.get('is_started', False):
            self.data.data['is_started'] = True
            self.__send_welcome_message()
            return

    def __send_welcome_message(self):
        api().send_message(self.user_id,
                           self.request_message,
                           reply_markup = self.add_markup)

    def finish(self, data: Dict):
        self.data.data['is_started'] = False
        super().finish(data)

