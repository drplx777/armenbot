from aiogram.fsm.state import StatesGroup, State

class Spam(StatesGroup):
    wait = State()

class Chat(StatesGroup):
    chat = State()