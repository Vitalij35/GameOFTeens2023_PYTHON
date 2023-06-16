from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from aiogram.types import Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hlink
from environs import Env

tar = [0, 0, 0, 0, 0, 0, 0]

env = Env()
env.read_env(".env")

bot = Bot(token=env.str("BOT_TOKEN"), parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class FSM(StatesGroup):
    Start = State()
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()


def start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Почнімо!😉'))
    return kb


def q1_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('До 10гб'), KeyboardButton('10-30гб👍'), KeyboardButton('Понад 30гб😎'))
    return kb


def q2_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Майже не телефоную🤫'), KeyboardButton('Іноді телефоную😀'),
           KeyboardButton('Постійно телефоную📞'))
    return kb


def q3_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Ніколи❌'), KeyboardButton('Інколи😀'), KeyboardButton('Досить часто😇'),
           KeyboardButton('Постійно🎖'))
    return kb


def q4_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Майже не буваю❌'), KeyboardButton('Інколи буваю😉'), KeyboardButton('Постійно буваю😎'))
    return kb


def q5_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Для себе📱'), KeyboardButton('Для дитини🧒'), KeyboardButton('Для планшету'),
           KeyboardButton('Для Ґаджету⌚️'))
    return kb


@dp.message_handler(commands="start")
async def start(message: Message):
    await message.answer("Привіт, я бот lifecell і я допоможу тобі обрати найкращий тариф! 😉\n"
                         "Все дуже просто!🤗 Тобі знадобится лише відповісти на 5 запитань\n"
                         "Натисни на клавішу «Почнімо!» щоб розпочати!",
                         reply_markup=start_kb())
    await FSM.Start.set()


@dp.message_handler(state=FSM.Start)
async def Q1(message: Message):
    if message.text == 'Почнімо!😉':
        await message.answer("Чудово!✨\n\n"
                             "Ось перше запитання:\n"
                             "Який обсяг інтернету ви зазвичай використовуєте?",
                             reply_markup=q1_kb())
        await FSM.Q1.set()


@dp.message_handler(state=FSM.Q1)
async def Q2(message: Message):
    global tar
    match message.text:
        case "До 10гб":
            tar[2] = tar[2] + 2
        case "10-30гб":
            tar[1] = tar[1] + 2
        case "Понад 30гб😎":
            tar[0], tar[3] = tar[0] + 2, tar[3] + 1

    await message.answer("2 запитання:\n"
                         "Як часто ви телефонуєте на номери інших операторів?",
                         reply_markup=q2_kb())
    await FSM.Q2.set()


@dp.message_handler(state=FSM.Q2)
async def Q3(message: Message):
    global tar
    match message.text:
        case "Майже не телефоную":
            tar[2] = tar[2] + 1
        case "Іноді телефоную":
            tar[1] = tar[1] + 1
        case "Постійно телефоную📞":
            tar[0], tar[3] = tar[0] + 1, tar[3] + 1

    await message.answer("3 запитання:\n"
                         "Як часто ви роздаєте інтернет?",
                         reply_markup=q3_kb())
    await FSM.Q3.set()


@dp.message_handler(state=FSM.Q3)
async def Q4(message: Message):
    global tar
    match message.text:
        case "Інколи😀":
            tar[1] = tar[1] + 1
        case "Досить часто😇":
            tar[1] = tar[1] + 2
        case "Постійно🎖":
            tar[1] = tar[1] + 3

    await message.answer("4 запитання:\n"
                         "Як часто ви буваєте за кордоном?",
                         reply_markup=q4_kb())
    await FSM.Q4.set()


@dp.message_handler(state=FSM.Q4)
async def Q5(message: Message):
    global tar
    match message.text:
        case "Інколи буваю":
            tar[3] = tar[3] + 1
        case "Постійно буваю😎":
            tar[3] = tar[3] + 3
    await message.answer("5 запитання:\n"
                         "Навіщо вам цей тариф?",
                         reply_markup=q5_kb())
    await FSM.Q5.set()


@dp.message_handler(state=FSM.Q5)
async def result(message: Message):
    tarif = 0
    max_bal = 0
    global tar
    match message.text:
        case "Для дитини🧒":
            tar[4] = tar[4] + 10
        case "Для планшету":
            tar[6] = tar[6] + 10
        case "Для Ґаджету⌚️":
            tar[5] = tar[5] + 10

    for i in range(0, len(tar)):
        if tar[i] > max_bal:
            max_bal = tar[i]
            tarif = i

    match tarif:
        case 0:
            text = hlink("Дізнатись більше", "https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/vilniy-life-2021/")
            await message.answer("<b>Вітаю, опитування завершено!</b>\n\n"
                                 "Тобі чудово підійде тариф «Вільний Лайф»!\n\n"
                                 "До нього входить безлімітний інтернет та 1600хв на двінки по Україні\n\n" + text)
        case 1:
            text = hlink("Дізнатись більше", "https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/smart-life-2021/")
            await message.answer("<b>Вітаю, опитування завершено!</b>\n\n"
                                 "Тобі чудово підійде тариф «Смарт Лайф»!\n\n"
                                 "До нього входить 25гб інтернету, 800хв на двінки по Україні, а ще безлім на соціальні мережі та безкоштовна роздача інтернету!\n\n" + text)
        case 2:
            text = hlink("Дізнатись більше", "https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/prosto-life-2021/")
            await message.answer("<b>Вітаю, опитування завершено!</b>\n\n"
                                 "Тобі чудово підійде тариф «Просто Лайф»!\n\n"
                                 "До нього входить 8гб інтернету та 300хв на двінки по Україні\n\n" + text)
        case 3:
            text = hlink("Дізнатись більше", "https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/platinum-life-2021/")
            await message.answer("<b>Вітаю, опитування завершено!</b>\n\n"
                                 "Тобі чудово підійде тариф «Platinum Лайф»!\n\n"
                                 "До нього входить безлімітний інтернет, 3000хв на двінки по Україні, роумінг та міжнародні дзвінки!\n\n" + text)
        case 4:
            text = hlink("Дізнатись більше", "https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/shkilniy/")
            await message.answer("<b>Вітаю, опитування завершено!</b>\n\n"
                                 "Тобі чудово підійде тариф «Шкільний Лайф»!\n\n"
                                 "До нього входить 7гб інтернету, безлім на lifecell, безлім на соціальні мережі та месенджери а також безліміт на два «Обрані номери»\n\n" + text)
        case 5:
            text = hlink("Дізнатись більше   ", "https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/gadget-bezpeka/")
            text2 = hlink("Дізнатись більше   ", "https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/gadget-smart21/")
            await message.answer("<b>Вітаю, опитування завершено!</b>\n\n"
                                 "Тобі чудово підійдуть тарифи «Ґаджет Безпека» та «Ґаджет Смарт»!\n\n"
                                 "До них входить 150-500мб інтернету на день, 15-50хв на дзвінки в мережі lifecell та 15-50 SMS в день!\n\n" + text + text2)
        case 6:
            text = hlink("Дізнатись більше", "https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/gadget-tab21/")
            await message.answer("<b>Вітаю, опитування завершено!</b>\n\n"
                                 "Тобі чудово підійде тариф «Ґаджет Планшет»!\n\n"
                                 "До нього входить 50гб інтернету, безлім на соціальні мережі то безкоштовна роздача інтернету!\n\n" + text)

    await message.answer("Спробувати ще раз?", reply_markup=start_kb())
    tar = [0, 0, 0, 0, 0, 0, 0]
    await FSM.Start.set()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
