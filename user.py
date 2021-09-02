
from typing import Dict

from telebot.types import Message

from blocks.phone_number import PhoneNumber
from blocks.first_name import FirstName
from blocks.last_name import LastName
from blocks.birth_date import BirthDate
from blocks.gender import Gender
from blocks.email import Email
from blocks.agreement import Agreement
from blocks.base import Subblocks
from blocks.children import Children


class User(Subblocks):
    _subblocks = [PhoneNumber, Agreement, FirstName, LastName,
                  BirthDate, Gender, Email, Children]
    _subblock = None

    block_id = 'user'