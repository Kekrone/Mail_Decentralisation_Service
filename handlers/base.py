from aiogram import Router, F
from aiogram.filters import CommandStart

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"Выберите действие",
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
    user_id = message.from_user.id
    await message.answer(f'{user_id} - MOmfsdfsdfsfsdfsdfsdf')