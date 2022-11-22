from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  # for reply keyboard (sends message)

from time import sleep


bot = Bot(token='test')
dp = Dispatcher(bot)

answers = []  # store the answers they have given

# Cinema Selection
Cine1 = KeyboardButton('Life Cinemas')
Cine2 = KeyboardButton('Movie Cinema')
Cine3 = KeyboardButton('Grupo Cine')
cine_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(Cine1).add(Cine2).add(Cine3)

# options selection: Life Cinemas
lc_options1 = KeyboardButton('Ver Ubicaciones')
lc_options2 = KeyboardButton('Ver Películas')
lc_options3 = KeyboardButton('Test')
lc_options_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(lc_options1).add(lc_options2).add(lc_options3)

# options selection: Movie Cinema
mc_options1 = KeyboardButton('Ver Ubicaciones')
mc_options2 = KeyboardButton('Ver Películas')
mc_options3 = KeyboardButton('Test')
mc_options_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(mc_options1).add(mc_options2).add(mc_options3)

# options selection: Movie Cinema
gc_options1 = KeyboardButton('Ver Ubicaciones')
gc_options2 = KeyboardButton('Ver Películas')
gc_options3 = KeyboardButton('Test')
gc_options_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(gc_options1).add(gc_options2).add(gc_options3)




#### selecting what you need
@dp.message_handler(regexp='Life Cinemas')
async def english(message: types.Message):
    answers.append(message.text)
    await message.answer('What do you need?', reply_markup = lc_options_kb)

#### selecting what you need
@dp.message_handler(regexp='Movie Cinema')
async def english(message: types.Message):
    answers.append(message.text)
    await message.answer('What do you need?', reply_markup = mc_options_kb)

#### selecting what you need
@dp.message_handler(regexp='Grupo Cine')
async def english(message: types.Message):
    answers.append(message.text)
    await message.answer('What do you need?', reply_markup = gc_options_kb)

# sends welcome message after start
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer('Hello! Por Favor seleccionar Zona', reply_markup=cine_kb)


# sends help message
@dp.message_handler(commands=['test'])
async def help(message: types.Message):
    await message.answer(
        'Esto es el test para la funcionalidad de telegram. Press /start to get started.')


# this is the last line
executor.start_polling(dp)