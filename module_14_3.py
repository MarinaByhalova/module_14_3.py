from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button1 = KeyboardButton(text='Информция')
button2 = KeyboardButton(text='Купить')
kb.row(button, button1)
kb.add(button2)

Inline_menu = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text='Рассчитать норму калорий'),
        KeyboardButton(text='Формулы расчёта')],
    resize_keyboard=True

)

mb = InlineKeyboardMarkup(resize_keyboard=True)
button_ = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button_1 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button_2 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button_3 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
mb.row(button_, button_1, button_2, button_3)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('1.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product 1| Описание: Апельсин| Цена: 100')
    with open('2.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product 2| Описание: Яблоко| Цена:  200')
    with open('3.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product 3| Описание: Вишня| Цена: 300')
    with open('4.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product 4| Описание: Банан| Цена: 400')
    await message.answer('Выберите продукт для покупки:', reply_markup=mb)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберете опцию:', reply_markup=Inline_menu)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(
        f'Ваша норма калорий:{int(data["weight"]) * 10 + int(data["growth"]) * 6.25 - int(data["age"]) * 5 + 5}')
    await state.finish()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.answer('Формула Миффлина-Сан Жеора: '
                      '(10 * вес + 6.25 * рост - 5 * возраст + 5)')


@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
