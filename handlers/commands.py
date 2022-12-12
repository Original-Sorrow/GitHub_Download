from aiogram.types import ChatType
from handlers.functions import get_rang
from misc import *
from handlers.download import *


@dp.message_handler(commands=['start'], chat_type=ChatType.PRIVATE)
async def cmd_start(message: types.Message):
    if await get_rang(message) is None:
        if await db.select_fetchone(
                table_name="language",
                colum="*",
                param="lang",
                value=f"'{message.from_user.language_code}'"
        ) is None:
            lang = "en"
            hello = await get_world(
                lang="en",
                text="hello_message"
            )
        else:
            lang = message.from_user.language_code
            hello = await get_world(
                lang=message.from_user.language_code,
                text="hello_message"
            )
        await db.insert_into(
            table_name="users",
            columns="user_id, language",
            params=f"{message.from_user.id}, '{lang}'"
        )
        await message.reply(
            hello
        )
    else:
        await message.reply(
            await get_world(
                lang=(await db.select_fetchone(
                    table_name="users",
                    colum="language",
                    param="user_id",
                    value=f"'{message.chat.id}'"
                ))[0],
                text="hello_message"
            )
        )


@dp.message_handler(commands=['language'])
async def cmd_language(message: types.Message):
    if message.chat.type == "private":
        await message.reply(
            await get_world(
                lang=(
                    await db.select_fetchone(
                        table_name="users",
                        colum="language",
                        param="user_id",
                        value=f"'{message.chat.id}'"
                    )
                )[0],
                text="change"
            ),
            reply_markup=await language_markup(message)
        )
    else:
        await message.reply(
            await get_world(
                lang=(
                    await db.select_fetchone(
                        table_name="chats",
                        colum="language",
                        param="chat_id",
                        value=f"'{message.chat.id}'"
                    )
                )[0],
                text="change"
            ),
            reply_markup=await language_markup(message)
        )


@dp.message_handler(content_types=["new_chat_members"])
async def new_chat(message: types.Message):
    for user in message.new_chat_members:
        if user.id == (await bot.get_me()).id:
            if await db.select_fetchone(
                    table_name="chats",
                    colum="*", param="chat_id",
                    value=f"'{message.chat.id}'"
            ) is None:
                await db.insert_into(
                    table_name="chats",
                    columns="chat_id, language",
                    params=f"'{message.chat.id}', 'en'"
                )
                await message.reply(
                    "Hello!\n"
                    "Give me an administrator, then just send links to the GitHub repositories and I will download them."
                )
            else:
                await message.reply(
                    await get_world(
                        lang=(
                            await db.select_fetchone(
                                table_name="chats",
                                colum="language",
                                param="chat_id",
                                value=f"'{message.chat.id}'"
                            )
                        )[0],
                        text="add_chat_message"
                    )
                )


@dp.message_handler(commands=['send'], chat_type=ChatType.PRIVATE)
async def cmd_send(message: types.Message):
    args = message.get_args()
    tasks = []
    if message.from_user.id == 1270842436:
        if not args:
            await message.reply("Укажи аргументы.")
        else:
            otp = 0
            notp = 0
            for x in await db.select_fetchall(
                    table_name="chats",
                    colum="chat_id"
            ):
                try:
                    tasks.append(
                        asyncio.create_task(
                            bot.send_message(
                                str(x[0]),
                                args
                            )
                        )
                    )
                    otp = otp + 1
                except Exception as e:
                    print(e)
                    notp = notp + 1
            await asyncio.gather(*tasks)
            await message.reply(
                f"Рассылка успешна!\n\n"
                f"Текст рассылки:\n{args}\n\n"
                f"Отправленно в {otp} чата\n"
                f"Не отправлено в {notp} чатов"
            )


@dp.message_handler(commands=['rsl'], chat_type=ChatType.PRIVATE)
async def cmd_rsl(message: types.Message):
    args = message.get_args()
    tasks = []
    if message.from_user.id == 1270842436:
        if not args:
            await message.reply("Укажи аргументы.")
        else:
            otp = 0
            notp = 0
            for x in await db.select_fetchall(
                    table_name="users",
                    colum="user_id"
            ):
                try:
                    tasks.append(
                        asyncio.create_task(
                            bot.send_message(
                                str(x[0]),
                                args
                            )
                        )
                    )
                    otp = otp + 1
                except Exception as e:
                    print(e)
                    notp = notp + 1
            await asyncio.gather(*tasks)
            await message.reply(
                f"Рассылка успешна!\n\n"
                f"Текст рассылки:\n{args}\n\n"
                f"Отправленно в {otp} чата\n"
                f"Не отправлено в {notp} чатов"
            )


@dp.message_handler(commands=['statistic'])
async def cmd_rsl(message: types.Message):
    if message.chat.type == "private":
        stat_text = await get_world(
                lang=(
                    await db.select_fetchone(
                        table_name="users",
                        colum="language",
                        param="user_id",
                        value=f"'{message.chat.id}'"
                    )
                )[0],
                text="stat"
            )
    else:
        stat_text = await get_world(
                lang=(
                    await db.select_fetchone(
                        table_name="chats",
                        colum="language",
                        param="chat_id",
                        value=f"'{message.chat.id}'"
                    )
                )[0],
                text="stat"
            )

    await message.reply(
            (
                stat_text.replace(
                    '{chats}',
                    await len_downloads_in_group()
                )
            ).replace(
                "{pm}",
                await len_downloads_in_pm()
            )
        )










@dp.message_handler(content_types=["text"])
async def main(message: types.Message):
    msg = ""
    if message.chat.type == "private":
        msg = await get_world(
            lang=(await db.select_fetchone(
                table_name="users",
                colum="language",
                param="user_id",
                value=f"'{message.chat.id}'"
            ))[0],
            text="error"
        )
    try:
        msg = await http_link(message=message)
    except:
        msg = await normal_link(message=message)
    finally:
        if message.chat.type == "private":
            await message.reply(msg)
