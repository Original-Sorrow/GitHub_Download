from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from misc import *
import datetime


async def today():
    return f"{datetime.datetime.now().day}.{datetime.datetime.now().month}.{datetime.datetime.now().year}"


async def add_static(message):
    if message.chat.type == "private":
        data = await db.select_fetchone(
            table_name="statistics",
            colum="count",
            param="(date, chat_type)",
            value=f"('{await today()}','private')"
        )
        if data is None:
            await db.insert_into(
                table_name="statistics",
                columns="date, chat_type, count",
                params=f"'{await today()}','private', 1"
            )
        else:
            await db.update(
                table_name="statistics",
                colum="count",
                colum_value=f"{int(data[0]) + 1}",
                param="(date, chat_type)",
                value=f"('{await today()}','private')"
            )
    else:
        data = await db.select_fetchone(
            table_name="statistics",
            colum="count",
            param="(date, chat_type)",
            value=f"('{await today()}','group')"
        )
        if data is None:
            await db.insert_into(
                table_name="statistics",
                columns="date, chat_type, count",
                params=f"'{await today()}','group', 1"
            )
        else:
            await db.update(
                table_name="statistics",
                colum="count",
                colum_value=f"{int(data[0]) + 1}",
                param="(date, chat_type)",
                value=f"('{await today()}','group')"
            )


async def get_rang(message):
    return await db.select_fetchone(
        table_name="users",
        colum="*", param="user_id",
        value=message.from_user.id
    )


async def get_world(lang: str, text: str):
    world = await db.select_fetchone(
        table_name="language",
        colum=text, param="lang",
        value=f"'{str(lang)}'"
    )
    if world is None:
        world = await db.select_fetchone(
            table_name="language",
            colum=text, param="lang",
            value="'en'"
        )
    return world[0]


async def get_project_name(link: str):
    text = link.split('/')
    text.remove('github.com')
    try:
        text.remove('https:')
    except:
        pass
    try:
        text.remove('')
    except:
        pass
    try:
        text.remove('http:')
    except:
        pass
    return str(text[1])


async def get_project_link(link: str):
    try:
        link = link.replace('https://', '')
    except:
        link = link.replace('http://', '')
    finally:
        link = link
    return str(link)


language_cb = CallbackData(
    'cat',
    'id',
    'lang',
    'action'
)


async def language_markup(message):
    markup = InlineKeyboardMarkup(
        resize_keyboard=True
    )
    global language_cb
    for lang in await db.select_fetchall(
            table_name="language",
            colum="lang"
    ):
        markup.add(
            InlineKeyboardButton(
                str(
                    lang[0]
                ),
                callback_data=language_cb.new(
                    id=message.chat.id,
                    lang=lang[0],
                    action="change_language")
            )
        )
    return markup


async def len_downloads_in_group():
    i = 0
    for x in await db.select_fetchall(
            table_name="statistics",
            colum="count",
            param="chat_type",
            value="'group'"
    ):
        x = int(x[0])
        i += x
    return str(i)


async def len_downloads_in_pm():
    i = 0
    for x in await db.select_fetchall(
            table_name="statistics",
            colum="count",
            param="chat_type",
            value="'private'"
    ):
        x = int(x[0])
        i += x
    return str(i)

# async def downloads_in_group(date: str):
#    return (await db.select_fetchone(
#        table_name="statistics",
#        colum="count",
#        param="(date, chat_type)",
#        value=f"('{date}','group')"
#    ))[0]


# async def downloads_in_pm(date: str):
#    return (await db.select_fetchone(
#        table_name="statistics",
#        colum="count",
#        param="(date, chat_type)",
#        value=f"('{date}','private')"
#    ))[0]
