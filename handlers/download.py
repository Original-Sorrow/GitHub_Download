import aiohttp
from handlers.functions import *


async def http_link(message):
    if message.chat.type == "private":
        link = await get_world(
            lang=(await db.select_fetchone(
                table_name="users",
                colum="language",
                param="user_id",
                value=f"'{message.chat.id}'"
            ))[0],
            text="link"
        )
        msg = await get_world(
            lang=(await db.select_fetchone(
                table_name="users",
                colum="language",
                param="user_id",
                value=f"'{message.chat.id}'"
            ))[0],
            text="error"
        )
    else:
        link = await get_world(
            lang=(await db.select_fetchone(
                table_name="chats",
                colum="language",
                param="chat_id",
                value=f"'{message.chat.id}'"
            ))[0],
            text="link"
        )
    async with aiohttp.ClientSession() as session:
        try:
            resp = await session.get(
                f'{message.text}/archive/refs/heads/master.zip'
            )
            await message.reply_document(
                (
                    f'{await get_project_name(link=message.text)}.zip',
                    resp.content
                ),
                caption=f'GitHub {link}: {await get_project_link(link=message.text)}'
            )
            msg = ""
            await add_static(message)
        except:
            resp = await session.get(
                f'{message.text[:1]}/archive/refs/heads/master.zip'
            )
            await message.reply_document(
                (f'{await get_project_name(link=message.text)}.zip',
                 resp.content
                 ),
                aption=f'GitHub {link}: {await get_project_link(link=message.text)}'
            )
            msg = ""
            await add_static(message)
    return msg


async def normal_link(message):
    if message.chat.type == "private":
        link = await get_world(
            lang=(await db.select_fetchone(
                table_name="users",
                colum="language",
                param="user_id",
                value=f"'{message.chat.id}'"
            ))[0],
            text="link"
        )
        msg = await get_world(
            lang=(await db.select_fetchone(
                table_name="users",
                colum="language",
                param="user_id",
                value=f"'{message.chat.id}'"
            ))[0],
            text="error"
        )
    else:
        link = await get_world(
            lang=(await db.select_fetchone(
                table_name="chats",
                colum="language",
                param="chat_id",
                value=f"'{message.chat.id}'"
            ))[0],
            text="link"
        )
    async with aiohttp.ClientSession() as session:
        try:
            resp = await session.get(
                f'http://{message.text}/archive/refs/heads/master.zip'
            )
            await message.reply_document(
                (
                    f'{await get_project_name(link=message.text)}.zip',
                    resp.content
                ),
                caption=f'GitHub {link}: {await get_project_link(link=message.text)}'
            )
            msg = ""
            await add_static(message)
        except:
            resp = await session.get(
                f'http://{message.text[:1]}/archive/refs/heads/master.zip'
            )
            await message.reply_document(
                (
                    f'{await get_project_name(link=message.text)}.zip',
                    resp.content),
                caption=f'GitHub {link}: {await get_project_link(link=message.text)}'
            )
            msg = ""
            await add_static(message)
    return msg
