from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    choose = State()
    mail_from = State()
    mail_to = State()
    del_mail_from = State()
    del_mail_to = State()