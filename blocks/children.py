

from typing import Dict
from copy import deepcopy

import localz
from singleton import api, logger
from .base import Block
from telebot.types import Message
from .ask_if_children import AskIfChildren
from .ask_if_more_child import AskIfMoreChild
from .child import Child


model_no = 'no'


class Children(Block):
    block_id = 'children'

    def __init__(self, user_id: int, callback: callable):
        super().__init__(user_id, callback)

        if not self.is_subblock_started():
            self.start_subblock(AskIfChildren, self.process_ask_if_children_result)

    def process_message(self, message: Message):
        if super().process_message(message):
            return

    def process_ask_if_children_result(self, data: Dict):
        result = data.get(AskIfChildren.block_id)
        if result == model_no:
            self.finish({self.block_id: []})
            return

        self.start_subblock(Child, self.process_child_result)

    def process_child_result(self, data: Dict):
        if self.data.data.get('children') is None:
            self.data.data['children'] = []
        self.data.data['children'].append(deepcopy(data))

        self.start_subblock(AskIfMoreChild, self.process_ask_if_more_child_result)

    def process_ask_if_more_child_result(self, data: Dict):
        result = data.get(AskIfMoreChild.block_id)

        if result == model_no:
            self.finish({self.block_id: self.data.data['children']})
            api().send_message(self.user_id, localz.children_saved)
            return

        self.start_subblock(Child, self.process_child_result)