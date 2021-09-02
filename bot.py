#!/usr/bin/python3

import os
from pprint import pformat
from typing import Dict
from user import User

import telebot
from telebot.types import Message
from singleton import logger, api
from rest_client import post_card_data
import singleton
import localz

import db


TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")


class Bot():
    #: telebot.TeleBot: instance of the bot API.
    _api = None

    def __init__(self, token: str):
        self._api = telebot.TeleBot(token = token, threaded = False)

        # Use custom handler adding instead of decorators.
        self._api.add_message_handler({
            # Read TeleBot.message_handler docstring for details.
            'function': self.get_message,
            'filters': {
                # content_types: ['audio', 'photo', 'voice', 'video',
                #     'document', 'text', 'location', 'contact', 'sticker']
                'content_types': ['audio', 'photo', 'voice', 'video',
                                  'document', 'text', 'location', 'contact',
                                  'sticker'],
                # commands=['start', 'help']
                'commands': None,
                # regexp='someregexp'
                'regexp': None,
                # if func returns True, the message will be passed to
                # the 'function'
                'func': lambda _message: True,
            }
        })

        self.__decorate_send_methods()

    def __decorate_send_methods(self):
        send_message = self._api.send_message

        def send_message_decorator(*args, **kwargs):
            logger.debug("Sending message: \n{}".format(args[1]))

            try:
                result = send_message(*args, **kwargs)
            except Exception:
                return send_message_decorator(*args, **kwargs)

            return result

        self._api.send_message = send_message_decorator

    def get_message(self, message: Message):
        raise NotImplementedError()

    def loop(self):
        singleton._api = self._api
        self._api.polling(none_stop = True)


class LoyaltyBot(Bot):
    def get_message(self, message: Message):
        logger.debug("Received a message: \n{}\n{}".format(message, pformat(message.json)))
        db.insert_message(message)

        user_id = message.from_user.id
        user = User(user_id = user_id,
                    callback = lambda data: self.callback(user_id, data))

        user.process_message(message)

    def callback(self, user_id: int, data: Dict):
        from pprint import pformat

        result = post_card_data(data)
        if result == 200:
            api().send_message(user_id, "Введені дані збережено 😊")
        else:
            api().send_message(user_id, localz.internal_server_error)


resender = LoyaltyBot(token = TELEGRAM_API_TOKEN)
resender.loop()
