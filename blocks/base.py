
from functools import lru_cache
from typing import Dict

from telebot.types import Message
from singleton import logger


class BlockData():
    user_id = None
    block_id = None
    subblock_index = 0
    data = None

    def __init__(self, user_id, block_id):
        self.user_id = user_id
        self.block_id = block_id
        self.data = {}

    # def pickle(self):
    #     pass

    # def unpickle(self):
    #     pass

    def save(self, data: Dict):
        self.data.update(data)

    def clear(self):
        self.data = {}


@lru_cache(maxsize = 1024)
def get_data(user_id, block_id):
    return BlockData(user_id, block_id)


class Block():
    #: callable: shall be called on block finish with the finish data.
    callback = None

    data = None
    block_id = 'block'

    def __init__(self, user_id: int, callback: callable):
        self.callback = callback
        logger.debug("Started block: {}".format(self.__class__.__name__))

        self.data = get_data(user_id, self.block_id)

    @property
    def user_id(self):
        return self.data.user_id

    def is_subblock_started(self):
        return bool(self.data.data.get('subblock_id'))

    def process_message(self, message: Message):
        logger.debug("{}: Processing message: \n{}".format(
            self.__class__.__name__,
            message.json))

        if self.is_subblock_started():
            self.pass_message_to_subblock(message)

            return True

        return False

    def pass_message_to_subblock(self, message: Message):
        subblock_id = self.data.data.get('subblock_id')
        subblock_callback = self.data.data.get('subblock_callback')
        from block_map import block_map
        block = block_map[subblock_id](message.from_user.id, subblock_callback)
        block.process_message(message)

    def finish(self, data: Dict):
        self.callback(data)
        self.data.clear()
        logger.debug("Finished block: {}: {}".format(
            self.__class__.__name__,
            data))

    def start_subblock(self, block, callback: callable):
        block_id = block.block_id
        def finish_subblock(data: Dict):
            self.data.save({'subblock_id': None, 'subblock_callback': None})
            callback(data)
        self.data.save({'subblock_id': block_id, 'subblock_callback': finish_subblock})
        instance = block(self.user_id, callback)


class Subblocks(Block):
    _subblocks = []
    _subblock = None

    block_id = 'subblocks'

    def __init__(self, user_id: int, callback: callable):
        super().__init__(user_id, callback)
        self._start_subblock()

    def process_message(self, message: Message):
        self._start_subblock()
        self._subblock.process_message(message)

    def __process_subblock_finish(self, data: Dict):
        self.data.save(data)
        self.data.subblock_index += 1

        if self.data.subblock_index >= len(self._subblocks):
            ## the last block returned data
            self.data.subblock_index = 0
            self.finish(self.data.data)
            return

        self._start_subblock()

    def _start_subblock(self):
        current_block = self._subblocks[self.data.subblock_index]
        self._subblock = current_block(self.user_id, self.__process_subblock_finish)
