# import math
# from datetime import datetime
#
# from loader import conn
# from utils.commands import find_exist_tg_user
# from utils.db_api.schemas.customer import telegram_user
# from utils.db_api.schemas.orders import curr_order
#
# a = 1
# b = 'false' if a == 0 else 'true'
# c = math.floor((a / 5) * 0.5)
# print(c)
#
# def find_exist_tg_user(msg_tgid):
#     find_exist_tg_user = telegram_user.select().where(telegram_user.c.tg_id == msg_tgid)
#     exist_tg_user = conn.execute(find_exist_tg_user).first()
#     return exist_tg_user
#
# def get_curr_user_order(msg_tgid):
#     exist_tg_user = find_exist_tg_user(msg_tgid)
#     exist_card_id = exist_tg_user[1]
#
#     get_exist_user_order = curr_order.select().where(curr_order.c.card_id == exist_card_id)
#     exist_user_order = conn.execute(get_exist_user_order).first()
#     place = exist_user_order[1]
#     hookah = exist_user_order[2]
#     open_order_time = exist_user_order[3]
#     tariff = exist_user_order[4]
#     duration = math.ceil(((datetime.now() - open_order_time).total_seconds())/60)
#
#     return place,hookah,duration,tariff
# try:
#     print(get_curr_user_order(305398726))
# except Exception as err:
#     print(err)
#
#

#
# a = [(8883, '1t', True, 2, 'min'), (6458, '1t', True, 2, 'min')]
# lena = len(a)
#
# for i in range(lena):
#     print(a[i][0])

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor


from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, DateTime

BOT_TOKEN = str("6279958249:AAFHXoApNlUhO3kbm8qnfYRVy58kn9dCRt0")

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

__all__ = ['bot', 'storage', 'dp', 'db']

meta = MetaData()

engine = create_engine('postgresql+psycopg2://postgres:1342@localhost:5432/dymok', echo=False)
meta.create_all(engine)
conn = engine.connect()

orders = Table('Orders', meta,
               Column('card_id', Integer),
               Column('place', String(100)),
               Column('hookah', Boolean),
               Column('open_order_time', DateTime),
               Column('close_order_time', DateTime),
               Column('order_duration', Integer),
               Column('tariff', String(100)),
               Column('bonus_add', Integer),
               Column('bonus_off', Integer),
               Column('total_cost', Integer)
               )


async def on_startup(dp):
    print('Бот запущен')


@dp.message_handler()
async def echo(msg: types.Message):
    select_exist_order = orders.select()
    answerss = conn.execute(select_exist_order).first()
    print(answerss)
    await msg.answer(answerss)


if __name__ == '__main__':
    try:
        executor.start_polling(dp, on_startup=on_startup, skip_updates=True, timeout=200000)
    except Exception as err:
        executor.start_polling(dp, on_startup=on_startup, skip_updates=True, timeout=200000)
        print(err)
