from aiogram import Router, F
from aiogram.filters import CommandStart

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

import dbmanager as dm

router = Router()

@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Выберите действие",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Добавить переадресацию"),
                    KeyboardButton(text="Удалить переадресацию")
                ],
                [
                    KeyboardButton(text='Получить список переадресаций')
                ]
            ],
            resize_keyboard=True,
        ),
    )

@router.message(F.text.casefold() == 'получить список переадресаций')
async def get_list_mails(message: Message):
    try:
        user_id = message.from_user.id
        string = ''
        answers = dm.get_user(user_id=user_id)
        if len(answers) != 0:
            for answer in answers:
                string += f'Почта отправитель: {answer[1]} -> Почта получатель: {answer[2]}\n\n'
            await message.answer(string)
        else:
            raise IndexError
    except IndexError:
        await message.answer("У вас нету сущевствующих переадресаций")