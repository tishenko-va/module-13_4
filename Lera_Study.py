from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup

api = "7660573003:AAHSSlMefukzZMRpM-kUneT_w_2wKcTcArA"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())



# @dp.message_handler(commands=['start'])
# async def start(message):
#      await message.answer(f'Привет! Я бот помогающий твоему здоровью.')

 # @dp.message_handler()
 # async def all_message(message):
 #     await message.answer(f'Введите команду /start, чтобы начать общение.')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
# #Функцию set_age(message):
# Оберните её в message_handler, который реагирует на текстовое сообщение 'Calories'.
# Эта функция должна выводить в Telegram-бот сообщение 'Введите свой возраст:'.
# После ожидать ввода возраста в атрибут UserState.age при помощи метода set.

@dp.message_handler(text= 'Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()
# Функцию set_weight(message, state):
# Оберните её в message_handler, который реагирует на переданное состояние UserState.growth.
# Эта функция должна обновлять данные в состоянии growth на message.text (написанное пользователем сообщение).
# Используйте метод update_data.
# Далее должна выводить в Telegram-бот сообщение 'Введите свой вес:'.
# После ожидать ввода роста в атрибут UserState.weight при помощи метода set.
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth= message.text)
    await message.answer('Введитк свой вес')
    await UserState.weight.set()

# Функцию send_calories(message, state):
# Оберните её в message_handler, который реагирует на переданное состояние UserState.weight.
# Эта функция должна обновлять данные в состоянии weight на message.text (написанное пользователем сообщение).
# Используйте метод update_data.
# Далее в функции запомните в переменную data все ранее введённые состояния при помощи state.get_data().
# Используйте упрощённую формулу Миффлина - Сан Жеора для подсчёта нормы калорий (для женщин или мужчин - на ваше усмотрение).
# Данные для формулы берите из ранее объявленной переменной data по ключам age, growth и weight соответственно.
# Результат вычисления по формуле отправьте ответом пользователю в Telegram-бот.
# Финишируйте машину состояний методом finish().

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f"Ваша норма в сутки {norma} ккал")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)