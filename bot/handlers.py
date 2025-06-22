import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from bot.generate import ai_generate
from bot.states import Spam, Chat
import bot.keyboards as kb

router = Router()


@router.message(F.text == 'Отмена')
@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer('Добро Пожаловать', reply_markup=kb.main)
    await message.answer('Если хотите задать вопрос нажмите кнопку - Чат')
    await state.clear()

@router.message(Spam.wait)
async def stop_spam(message: Message):
    await message.answer('Подождите пока обработается запрос')

@router.message(F.text == 'Чат')
async def chatting(message: Message, state: FSMContext):
    await message.answer('Задайте вопрос', reply_markup=kb.cancel)
    await state.set_state(Chat.chat)

@router.message(F.sticker)
async def sticker(message: Message):
    await message.answer('В данный момент, я не умею обрабатывать стикеры')

@router.message(F.video)
async def video(message: Message):
    await message.answer('В данный момент, я не умею обрабатывать видео')

@router.message(Chat.chat)
async def generate(message: Message, state: FSMContext):
    await state.set_state(Spam.wait)
    response= await ai_generate(message.text)
    await message.answer(response)
    await state.clear()
    await state.set_state(Chat.chat)


       