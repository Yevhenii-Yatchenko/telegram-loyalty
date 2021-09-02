
from blocks.child_first_name import ChildFirstName
from blocks.child_gender import ChildGender
from blocks.child_birth_date import ChildBirthDate
from blocks.base import Subblocks


class Child(Subblocks):
    _subblocks = [ChildFirstName, ChildGender, ChildBirthDate]

    block_id = 'child'
