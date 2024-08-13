from aiogram.fsm.state import StatesGroup, State


class SendNewsForm(StatesGroup):
    message = State()


class CallCommandForm(StatesGroup):
    message = State()


class SendIssueForm(StatesGroup):
    fio = State()
    place = State()
    problem = State()


class SuggestIdeaForm(StatesGroup):
    fio = State()
    idea = State()


class AnswerForm(StatesGroup):
    text = State()


class DirectSendForm(StatesGroup):
    text = State()
