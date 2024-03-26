from string import ascii_lowercase

from aiogram import Router, F
from aiogram.enums import ParseMode
from email_validator import EmailNotValidError, validate_email

from states import Form
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

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
        await state.update_data(mail_f=message.text)
        await message.answer(text="Введите целевую почту")
        await state.set_state(Form.del_mail_to)
    else:
        await state.set_state(Form.del_mail_from)
        await message.answer(text="Название для почты не должно содержать `@доменное_имя`",
                             parse_mode=ParseMode.MARKDOWN)


@router.message(Form.del_mail_to)
async def delete_mail_to(message: Message, state: FSMContext) -> None:
    if check(message.text):
        await state.update_data(mail_t=message.text)
        await message.answer(text=str(await state.get_data()))
        await state.clear()
    else:
        await message.answer(text="*Некорректный* формат почты. Попробуйте еще раз!",
                             parse_mode=ParseMode.MARKDOWN)
        await state.set_state(Form.del_mail_to)
