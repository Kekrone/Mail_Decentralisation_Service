from aiogram import Router, F
from states import Form
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums import ParseMode

from email_validator import validate_email, EmailNotValidError

import dbmanager as dm
import terminal as tm


router = Router()

def check(email):
    try:
        v = validate_email(email)
        email = v.normalized
        return True
    except EmailNotValidError:
        return False

@router.message(F.text.casefold() == "добавить переадресацию")
async def add_mail(message: Message, state: FSMContext) -> None:
    await message.answer(text="Введите псевдоним")
    await state.set_state(Form.mail_from)


@router.message(Form.mail_from)
async def add_mail_from(message: Message, state: FSMContext) -> None:
    if check(message.text + '@apethrone.ru'):
        await state.update_data(mail_f=message.text)
        await message.answer(text="Введите целевую почту")
        await state.set_state(Form.mail_to)
    else:
        await state.set_state(Form.mail_from)
        await message.answer(text="Название для почты не должно содержать `@доменное_имя` или латинские буквы", parse_mode=ParseMode.MARKDOWN)



@router.message(Form.mail_to)
async def add_mail_to(message: Message, state: FSMContext) -> None:
    if check(message.text):
        await state.update_data(mail_t=message.text)
        data = await state.get_data()
        user_id = message.from_user.id
        dm.register_user(user_id=user_id, source=data['mail_f'] + '@apethrone.ru', destination=data['mail_t'])
        tm.add_to_ubuntu(name=data['mail_f'])
        await message.answer(f'Успешно добавлена переадресация с {data['mail_f'] + '@apethrone.ru'} на {data['mail_t']}')
        await state.clear()
    else:
        await state.set_state(Form.mail_to)
        await message.answer(text="Некорректный формат почты. Попробуйте еще раз!")

