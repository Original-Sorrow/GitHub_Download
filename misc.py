import asyncio, config
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DB.database import DB

db = DB(
    host=config.host_db,
    user=config.user,
    password=config.password,
    database=config.database
)
bot = Bot(
    config.BOT_TOKEN,
    parse_mode=types.ParseMode.HTML
)
dp = Dispatcher(
    bot=bot,
    storage=MemoryStorage(),
    loop=asyncio.get_event_loop()
)
