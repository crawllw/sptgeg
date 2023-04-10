from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor


from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, DateTime

BOT_TOKEN = str("")

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

URL_APP = 'http://v1772047.hosted-by-vdsina.ru/'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 5000

async def onstartup(dp):
    try:
        await bot.set_webhook(URL_APP)
        print('Бот запущен')
    except Exception:
        print('ERROR')


async def onshutdown(dp):
    print('Bot closed')
    await bot.delete_webhook()


if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path='',
        skip_updates=True,
        on_startup=onstartup,
        on_shutdown=onshutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


