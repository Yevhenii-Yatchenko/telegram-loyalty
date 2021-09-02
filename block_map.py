from blocks.ask_if_children import AskIfChildren
from blocks.ask_if_more_child import AskIfMoreChild
from blocks.agreement import Agreement
from blocks.answer_requestor import AnswerRequestor
from blocks.ask_if_children import AskIfChildren
from blocks.base import Block
from blocks.base import Subblocks
from blocks.birth_date import BirthDate
from blocks.child_birth_date import ChildBirthDate
from blocks.child_first_name import ChildFirstName
from blocks.child_gender import ChildGender
from blocks.child import Child
from blocks.children import Children
from blocks.email import Email
from blocks.first_name import FirstName
from blocks.gender import Gender
from blocks.last_name import LastName
from blocks.phone_number import PhoneNumber

block_map = {
    Agreement.block_id: Agreement,
    AnswerRequestor.block_id: AnswerRequestor,
    AskIfChildren.block_id: AskIfChildren,
    AskIfMoreChild.block_id: AskIfMoreChild,
    Block.block_id: Block,
    Subblocks.block_id: Subblocks,
    BirthDate.block_id: BirthDate,
    ChildBirthDate.block_id: ChildBirthDate,
    ChildFirstName.block_id: ChildFirstName,
    ChildGender.block_id: ChildGender,
    Child.block_id: Child,
    Children.block_id: Children,
    Email.block_id: Email,
    FirstName.block_id: FirstName,
    Gender.block_id: Gender,
    LastName.block_id: LastName,
    PhoneNumber.block_id: PhoneNumber,
}