import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from peewee import *
import csv
import pandas as pd


if True:
    bot = Bot(token = '5911708501:AAEQb4eMCorzrO601whwalTovvQmfttKo0A')
    #dp = Dispatcher(bot)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    card = ""
    cards = {"DT": "Дебетовая карта Тинькофф",
             "CT": "Кредитная карта Тинькофф",
             "DA": "Дебетовая карта Альфа",
             "CA": "Кредитная карта Альфа",
             "DO": "Дебетовая карта Открытие",
             "CO": "Кредитная карта Открытие",
             "DM": "Дебетовая карта Московский Кредитный Банк",
             "CM": "Кредитная карта Московский Кредитный Банк",
    }


    #df = pd.DataFrame({"name": [], "number": [], "card": []})

    df = pd.read_csv("users.csv", index_col=[0])

    sl = {"name": "", "number": ""}

    text={
        "Welcome": "",

        "HowWorks": "🟢  Как это работает? \n В основе работы бота лежит акция «Приведи друга», проводимая многими российскими банками для привлечения клиентов. \
        \n По этой программе, приводящая сторона, которой является данный бот, получает денежное вознаграждение за каждого приведенного пользователя. \
        \n Данное вознаграждение зависит от условий акции «приведи друга», с ними вы можете ознакомится при выборе счета/карты. \
        \n Приведенный клиент получает продукт на льготных условиях, например с бесплатным обслуживанием или повышенным кэшбеком. \
        \n 🟢 ПОЧЕМУ ИМЕННО ЭТОТ БОТ? \
        \n Позволяет не только открыть счет на выгодных условиях, но и заработать с этого \
        \n Отслеживает, кто открыл счет и выполнил условия по нашим ссылкам \
        \n Платит 70 % от полученных средств, ВАМ \
        \n 🟢 ВАМ НУЖНО: \
        \n1. Выбрать желаемый банк и карту; \
        \n2. Ознакомиться с условиями открытия и получаемыми бонусами; \
        \n3. Зарегистрировать ваш профиль(это поможет нам быстрее идентифицировать, что это именно вы, создали карту по нашей ссылке и перевести вам деньги); \
        \n4. Открыть счет и выполнить условия; \
        \n5. Бот получит вознаграждение и переведет 70% суммы по вашим банковским реквизитам, указанным в профиле; \
        \n ⚠️Будьте внимательны⚠️\
        \n БанковскаяХаляваБот не несет ответственности за неправильно указанные данные. В данном случае, мы никак не сможем вам помочь",


        "Tinkoff": "🟡 Для получения бонуса по нашей программе, у вас не должны быть открыты счета и карты той же категории в «Тинькофф». Если вы уже участвовали в акции «Приведи друга», то нужно,\
    чтобы с тех пор прошло не меньше года",
        "Alpha": "🟡 Для получения бонуса по нашей программе, у вас не должны быть открыты счета и карты той же категории в «Альфа Банке».",
        "Open": "🟡 Для получения бонуса по нашей программе, у вас не должны быть открыты счета и карты той же категории в «Банке Открытие».",
        "MosCard": "🟡 Для получения бонуса по нашей программе, у вас не должны быть открыты счета и карты той же категории в «Московском Кредитном Банке»",


        "AttentionTinkoff": "",
        "AttentionAlpha": "",
        "AttentionOpen": "",
        "AttentionMos": "",


        "DebetTinkoff": "🟡Дебетовая карта Tinkoff Black \n\
        \nУСЛОВИЯ ПОЛУЧЕНИЯ: \
        \n1. Активировать полученную карту, совершив покупки на 300 рублей. \n\
        \nВОЗНАГРАЖДЕНИЯ: \
        \n1. 300 рублей; \
        \n2. Повышенный кэшбек; \
        \n3. Бесплатное обслуживание навсегда. \n\
        \nПеред открытием счета, пожалуйста введите данные, которые помогут нам убедиться в выполнение условий открытия счет",

        "CreditTinkoff": "🟡Кредитная карта Tinkoff Platinum \
        \nВозраст получения 18+ \n\
        \nУСЛОВИЯ ПОЛУЧЕНИЯ: \
        \n1. Активировать полученную карту, совершив покупки на 1500 рублей. \n \
        \nВОЗНАГРАЖДЕНИЯ: \
        \n1. 1500 рублей; \
        \n2. Повышенный кэшбек; \
        \n3. Бесплатное обслуживание навсегда. \n\
        \nПеред открытием счета, пожалуйста введите данные, которые помогут нам убедиться в выполнение условий открытия счета.",

        "DebetAlpha": "T",

        "CreditAlpha": "T",

        "DebetOpen": "🟡Дебетовая карта Открытие \n\
        \nУСЛОВИЯ ПОЛУЧЕНИЯ: \
        \n1. Активировать полученную карту, совершив покупки на 1500 рублей в течение 30 календарных дней\n\
        \nВОЗНАГРАЖДЕНИЯ: \
        \n1. 500 баллов (1 балл = 1 рубль); \
        \n2. 500 рублей.\n\
        \nПеред открытием счета, пожалуйста введите данные, которые помогут нам убедиться в выполнение условий открытия счета",

        "CreditOpen": "🟡Кредитная карта Открытие \
        \n Возраст получения 18+\n\
        \n УСЛОВИЯ ПОЛУЧЕНИЯ: \
        \n 1. Активировать полученную карту, совершив покупки на 3000 рублей в течение 30 календарных дней; \n\
        \n ВОЗНАГРАЖДЕНИЯ:\
        \n 1. 3000 баллов (1 балл = 1 рубль); \
        \n 2. 1200 рублей \n\
        \n Перед открытием счета, пожалуйста введите данные, которые помогут нам убедиться в выполнение условий открытия счета",

        "DebetMos": "🟡Дебетовая карта Москарта\n\
        \nУСЛОВИЯ ПОЛУЧЕНИЯ БОНУСА: \
        \n1. Активировать полученную карту, совершив покупку;\
        \n2. Зарегистрироваться в программе «МКБ Бонус».\n\
        \nВОЗНАГРАЖДЕНИЕ:\
        \n1. 500 баллов (1 балл = 1 рубль);\
        \n2. 500 рублей.\
        \nПеред открытием счета, пожалуйста введите данные, которые помогут нам убедиться в выполнение условий открытия счета\
        \n\n\n🟡Дебетовая карта Москарта Black \n\
        \n УСЛОВИЯ ПОЛУЧЕНИЯ БОНУСА: \
        \n1. Активировать полученную карту, совершив покупку;\
        \n2. Зарегистрироваться в программе «МКБ Бонус».\n\
        \nВОЗНАГРАЖДЕНИЕ:\
        \n1. 1000 баллов (1 балл = 1 рубль);\
        \n2. 400 рублей.\n\
        \nПеред открытием счета, пожалуйста введите данные, которые помогут нам убедиться в выполнение условий открытия счета",



        "CreditMos": "🟡Кредитная карта «Можно больше»\
        \nСтрого 18+\n\
        \nУСЛОВИЯ ПОЛУЧЕНИЯ БОНУСА:\
        \n1. Активировать полученную карту, совершив покупку\
        \n2. Зарегистрироваться в программе «МКБ Бонус»\n\
        \nВОЗНАГРАЖДЕНИЕ:\
        \n1. 1000 баллов (1 балл = 1 рубль);\
        \n2. 400 рублей.\n\
        \nПеред открытием счета, пожалуйста введите данные, которые помогут нам убедиться в выполнение условий открытия счета",


        "inputname": "Введите ФИО:",
        "number": "Введите номер карты:"
    }

class Form(StatesGroup):
    card = State()
    name = State()
    age = State()


def start_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Как это работает?", callback_data="HowWorks"),
            types.InlineKeyboardButton(text="Каталог банков", callback_data="catalog")
        ],
        [types.InlineKeyboardButton(text="Поддержка", url="https://t.me/BankfreebieHelp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def return_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Каталог банков", callback_data="catalog")
        ],
        [types.InlineKeyboardButton(text="Поддержка", url="https://t.me/BankfreebieHelp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def reply_keyboard():
    kb = [
        [
            types.KeyboardButton(text="/start")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

def bank_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Тинькофф",
                                       callback_data="tinkoff"),
            types.InlineKeyboardButton(text="Альфа", callback_data="alpha")
        ],
        [
            types.InlineKeyboardButton(text="Открытие",
                                       callback_data="open"),
            types.InlineKeyboardButton(text="Московский кредитный банк", callback_data="Mos")
        ],
        [types.InlineKeyboardButton(text="Поддержка", url = "https://t.me/BankfreebieHelp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def choose_card(bank):
    buttons = [
                  [
                      types.InlineKeyboardButton(text="Дебетовая",
                                                 callback_data="Debet"+str(bank)),
                      types.InlineKeyboardButton(text="Кредитная", callback_data="Credit"+str(bank))
                  ],
                [
                    types.InlineKeyboardButton(text="Меню",
                                               callback_data="Menu"),
                    types.InlineKeyboardButton(text="Каталог банков", callback_data="catalog")
                ],

        [types.InlineKeyboardButton(text="Поддержка", url="https://t.me/BankfreebieHelp")]
            ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def debet_tinkoff():
    buttons = [

        [
            types.InlineKeyboardButton(text="Ввести данные",
                                       callback_data="DataDT"),
        ],

        [types.InlineKeyboardButton(text="Поддержка", url="https://t.me/BankfreebieHelp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def credit_tinkoff():
    buttons = [

        [
            types.InlineKeyboardButton(text="Ввести данные",
                                       callback_data="DataCT"),
        ],

        [types.InlineKeyboardButton(text="Поддержка", url="https://t.me/BankfreebieHelp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def debet_alpha():
    buttons = [

        [
            types.InlineKeyboardButton(text="Ввести данные",
                                       callback_data="DataDA"),
        ],

        [types.InlineKeyboardButton(text="Поддержка", url="https://t.me/BankfreebieHelp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def credit_alpha():
    buttons = [

        [
            types.InlineKeyboardButton(text="Ввести данные",
                                       callback_data="DataCA"),
        ],

        [types.InlineKeyboardButton(text="Поддержка", url="https://t.me/BankfreebieHelp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def debet_open():
    buttons = [

        [
            types.InlineKeyboardButton(text="Ввести данные",
                                       callback_data="DataDO"),
        ],

        [types.InlineKeyboardButton(text="Поддержка", url="https://t.me/BankfreebieHelp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def credit_open():
    buttons = [

        [
            types.InlineKeyboardButton(text="Ввести данные",
                                       callback_data="DataCO"),
        ],

        [types.InlineKeyboardButton(text="Поддержка", url="https://t.me/BankfreebieHelp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def debet_mos():
    buttons = [

        [
            types.InlineKeyboardButton(text="Ввести данные",
                                       callback_data="DataDM"),
        ],

        [types.InlineKeyboardButton(text="Поддержка", url="https://t.me/BankfreebieHelp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def credit_mos():
    buttons = [

        [
            types.InlineKeyboardButton(text="Ввести данные",
                                       callback_data="DataCM"),
        ],

        [types.InlineKeyboardButton(text="Поддержка", url="https://t.me/BankfreebieHelp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def confirm_keyboard():
    buttons = [

        [
            types.InlineKeyboardButton(text="Подтвердить",
                                       callback_data="confirm"),
        ],

        [
            types.InlineKeyboardButton(text="Изменить данные",
                                       callback_data="change"),
        ],

        [
            types.InlineKeyboardButton(text="Каталог банков",
                                       callback_data="catalog"),
        ],

        [types.InlineKeyboardButton(text="Поддержка", url="https://t.me/BankfreebieHelp")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@dp.message_handler(commands=['start'])
async def process_command_1(message: types.Message):
    print("Тык старт " + str(message.chat.id))
    await bot.send_message(chat_id = message.chat.id, text = "🟡 Вас приветствует БанковскаяХаляваБот, который поможет вам выгодно открыть счет в банке", reply_markup=start_keyboard())


@dp.callback_query_handler(lambda c: c.data == 'Menu')
async def process_callback_menu(callback_query: types.CallbackQuery):
    print("Тык 1 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '🟡 Вас приветствует БанковскаяХаляваБот, который поможет вам выгодно открыть счет в банке', reply_markup=start_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'HowWorks')
async def process_callback_menu(callback_query: types.CallbackQuery):
    print("Тык 0 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["HowWorks"], reply_markup=return_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'catalog')
async def process_callback_catalog(callback_query: types.CallbackQuery):
    print("Тык 2 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '🟡 Выберите желаемый банк:', reply_markup=bank_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'tinkoff')
async def process_callback_tinkoff(callback_query: types.CallbackQuery):
    print("Тык 3 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["Tinkoff"], reply_markup=choose_card("Tinkoff"))

@dp.callback_query_handler(lambda c: c.data == 'alpha')
async def process_callback_alpha(callback_query: types.CallbackQuery):
    print("Тык 4 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["Alpha"], reply_markup=choose_card("Alpha"))

@dp.callback_query_handler(lambda c: c.data == 'open')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print("Тык 5 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["Open"], reply_markup=choose_card("Open"))

@dp.callback_query_handler(lambda c: c.data == 'Mos')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print("Тык 6 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["MosCard"], reply_markup=choose_card("Mos"))


#Дебетовая или Кредитная карта
@dp.callback_query_handler(lambda c: c.data == 'DebetTinkoff')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print("Тык 7 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["DebetTinkoff"], reply_markup=debet_tinkoff())

@dp.callback_query_handler(lambda c: c.data == 'CreditTinkoff')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print("Тык 8 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["CreditTinkoff"], reply_markup=credit_tinkoff())

@dp.callback_query_handler(lambda c: c.data == 'DebetAlpha')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print("Тык 9 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["DebetAlpha"], reply_markup=debet_alpha())

@dp.callback_query_handler(lambda c: c.data == 'CreditAlpha')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print("Тык 10 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["CreditAlpha"], reply_markup=credit_alpha())

@dp.callback_query_handler(lambda c: c.data == 'DebetOpen')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print("Тык 11 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["DebetOpen"], reply_markup=debet_open())

@dp.callback_query_handler(lambda c: c.data == 'CreditOpen')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print("Тык 12 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["CreditOpen"], reply_markup=credit_open())

@dp.callback_query_handler(lambda c: c.data == 'DebetMos')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print("Тык 11 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["DebetMos"], reply_markup=debet_mos())

@dp.callback_query_handler(lambda c: c.data == 'CreditMos')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print("Тык 12 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text["CreditMos"], reply_markup=credit_mos())





#Вводим ФИО
@dp.callback_query_handler(lambda c: c.data == 'DataDT')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global card
    card = "DT"
    print("Тык 13 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await Form.name.set()
    await bot.send_message(callback_query.from_user.id, text["inputname"])

#Вводим ФИО
@dp.callback_query_handler(lambda c: c.data == 'DataСT')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global card
    card = "CT"
    print("Тык 14 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await Form.name.set()
    await bot.send_message(callback_query.from_user.id, text["inputname"])

#Вводим ФИО
@dp.callback_query_handler(lambda c: c.data == 'DataDA')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global card
    card = "DA"
    print("Тык 15 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await Form.name.set()
    await bot.send_message(callback_query.from_user.id, text["inputname"])

#Вводим ФИО
@dp.callback_query_handler(lambda c: c.data == 'DataCA')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global card
    card = "CA"
    print("Тык 16 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await Form.name.set()
    await bot.send_message(callback_query.from_user.id, text["inputname"])

#Вводим ФИО
@dp.callback_query_handler(lambda c: c.data == 'DataDO')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global card
    card = "DO"
    print("Тык 17 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await Form.name.set()
    await bot.send_message(callback_query.from_user.id, text["inputname"])

#Вводим ФИО
@dp.callback_query_handler(lambda c: c.data == 'DataCO')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global card
    card = "CO"
    print("Тык 18 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await Form.name.set()
    await bot.send_message(callback_query.from_user.id, text["inputname"])

#Вводим ФИО
@dp.callback_query_handler(lambda c: c.data == 'DataDM')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global card
    card = "DM"
    print("Тык 19 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await Form.name.set()
    await bot.send_message(callback_query.from_user.id, text["inputname"])

#Вводим ФИО
@dp.callback_query_handler(lambda c: c.data == 'DataCM')
async def process_callback_button1(callback_query: types.CallbackQuery):
    global card
    card = "CM"
    print("Тык 20 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await Form.name.set()
    await bot.send_message(callback_query.from_user.id, text["inputname"])


# Добавляем возможность отмены, если пользователь передумал заполнять
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')


# Сюда приходит ответ с именем
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        sl["name"] = data["name"]
    await Form.next()
    await message.reply("Введите номер карты:")


# Проверяем возраст
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def process_age_invalid(message: types.Message):
    return await message.reply("Введите номер карты или напиши /cancel")



# Сохраняем возраст, выводим анкету
@dp.message_handler(state=Form.age)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data["card"] = card
            data['number'] = message.text
            sl["number"] = data['number']
            sl["card"] = card
            markup = types.ReplyKeyboardRemove()

            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text("Проверьте данные: \n"),
                    md.text('ФИО:', md.bold(data['name']), "\n"),
                    md.text('Номер карты:\n', md.code(data['number']), "\n"),
                    md.text('Тип карты: \n', md.code(cards[data['card']])),
                    sep='\n',
                ),
                reply_markup=confirm_keyboard(),
                parse_mode=ParseMode.MARKDOWN,
            )
        except:
            await bot.send_message(
                message.chat.id, "Начните заново: выберите нужную карту и введите свои данные еще раз", reply_markup=return_keyboard())

    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'confirm')
async def process_callback_menu(callback_query: types.CallbackQuery):
    print("Тык 21 " + str(callback_query.chat_instance))
    try:
        sl["id"] = str(callback_query.chat_instance)
        print(df)
        print([sl["name"], sl["number"], cards[sl["card"]]])
        df.loc[str(sl["id"])+" "+str(sl["card"])] = [sl["name"], sl["number"], cards[sl["card"]]]
        print(df)
        df.to_csv("users.csv")
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "🟡 Вы успешно ввели данные. Теперь вы можете открыть банковский счет! \
        \nСсылка для открытия счета:  https://www.tinkoff.ru/sl/3wJZvX6czp", reply_markup=start_keyboard())
    except:
        await bot.send_message(callback_query.from_user.id, "Начните заново: выберите нужную карту и введите свои данные еще раз", reply_markup=return_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'change')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print("Тык 22 " + str(callback_query.chat_instance))
    await bot.answer_callback_query(callback_query.id)
    await Form.name.set()
    await bot.send_message(callback_query.from_user.id, text["inputname"])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
