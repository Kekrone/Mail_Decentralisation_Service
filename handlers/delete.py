from string import ascii_lowercase

from aiogram import Router, F
from aiogram.enums import ParseMode
from email_validator import EmailNotValidError, validate_email

from states import Form
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import dbmanager as dm
import terminal as tm

router = Router()

def check(email):
    try:
        v = validate_email(email)
        email = v.normalized
        return True
    except EmailNotValidError as e:
        return False

@router.message(F.text.casefold() == "удалить переадресацию")
async def delete_mail(message: Message, state: FSMContext) -> None:
    await message.answer(text="Введите псевдоним")
    await state.set_state(Form.del_mail_from)


@router.message(Form.del_mail_from)
async def delete_mail_from(message: Message, state: FSMContext) -> None:
    if not check(message.text) and all([x.lower() in ascii_lowercase for x in message.text]):
        mail_f = message.text + '@apethrone.ru'
        await state.clear()
        dm.delete_user(source=mail_f)
        tm.delete_user(name=message.text)
        await message.answer('Успешно')
    else:
        await state.set_state(Form.del_mail_from)
        await message.answer(text="Название для почты должно содержать `@доменное_имя`",
                             parse_mode=ParseMode.MARKDOWN)
