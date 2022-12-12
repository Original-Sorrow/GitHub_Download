from aiogram.types import CallbackQuery
from handlers.functions import *
from misc import *


@dp.callback_query_handler(language_cb.filter(action='change_language'))
async def category_callback_handler(query: CallbackQuery, callback_data: dict):
    if int(callback_data["id"]) < 0:
        await db.update(
            table_name="chats",
            colum="language",
            colum_value=f"'{callback_data['lang']}'",
            param="chat_id",
            value=f"'{callback_data['id']}'"
        )
        await bot.delete_message(query.message.chat.id, query.message.message_id)
        await bot.send_message(query.message.chat.id, f"{await get_world(lang=callback_data['lang'], text='changed')} <b>{callback_data['lang']}</b>")
    else:
        await db.update(
            table_name="users",
            colum="language",
            colum_value=f"'{callback_data['lang']}'",
            param="user_id",
            value=callback_data['id']
        )
        await bot.delete_message(query.message.chat.id, query.message.message_id)
        await bot.send_message(query.message.chat.id, f"{await get_world(lang=callback_data['lang'], text='changed')} <b>{callback_data['lang']}</b>")
