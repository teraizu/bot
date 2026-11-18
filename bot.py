
from telethon import TelegramClient, events
from telethon.errors import ChannelPrivateError
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

api_id = 30483590
api_hash = "632d5dfdbca4d0a3a20b1acb0b3019ed"

bot_token = "8629856270:AAEb1jSTvH6abj4DG8V0ixEn3Ydb_UO59qQ"

receiver_chat_id = -1003952203212

source_chats = [
    -1002250763892,
    -1002045319553,
    -1003168528054,
    -1002295456779,
    -1002653439268,
    -1001721703585,
    -1002182974459,
    -1003866890652,
    -1002530504265,
    -1001862959901,
    -1003860219233,
    -1002246400032,
    -1002641367415,
    -1002054974885,
    -1003102414303,
    -1003747400268,
    -1003131012116,
    -1003757887087,
    -1001437845679,
    -1001541735085,
    -1002513806720,
    -1002450196082,
    -1002266940236,
    -1002099746177,
    -1001611791779,
    -1001474589396,
    -1001818263204,
    -1002241138883,
    -1002705210864,
    -1001559347062,
    -1002099478524,
    -1001626921364,
    -1001780203965,
    -1003116535447,
    -1002306213344,
    -1002418703723,
    -1002108698820,
    -1003737287920,
    -1001532493523,
    -1001973897082,
    -1002048601247,
    -1001813559130,
    -1003911110097,
    -1001741805570,
    -1001678861400,
    -1001653835982,
    -1001917268514,
    -1001459285527,
    -1001849495976,
    -1001766833393,
    -1002311278100,
    -1003130883689,
    -1002219933906,
    -1003892456593,
    -1003393464884,
    -1003952248909,
    -1001795429833,
    -1002425533128,
    -1003782398980,
    -1001662480610,
    -1003340630841,
    -1003636853824,
    -1001404838809,
    -1002803710458,
    -1003601779239,
    -1002456358731,
    -1002428776248,
    -1001705155335,
    -1002645722505,
    -1001693896351,
    -1001921513775,
    -1001599364240,
    -1002086773833,
    -1001546809504,
    -1003357114751,
    -1001589630281,
    -1001468259614,
    -1001920189835,
    -1003398586849,
    -1001821560564,
    -1003860959037,
    -1004355253400,
    -1001693007555,
    -1001892660479,
    -1002326171537,
    -1003577743259,
    -1002952138862,
    -1003788696315,
    -1001653940655,
    -1001276270034,
    -1002084923358,
    -1002477454794,
    -1003980216790,
    -1001816913995,
    -1002294656646,
    -1004450033009,
    -1003742058940,
    -1003998299377,
    -1001645647520,
    -1004497225254,
    -1001742626297,
    -1003555705392,
    -1004320034224,
    -1004297934618,
    -1003989973325,
    -1002276803902,
    -1002594312744,
    -1003344715017
]


client = TelegramClient(
    "bot_session_1",
    api_id,
    api_hash
)

bot = Bot(token=bot_token)


# -------------------------
# 💾 ПАМЯТЬ ПОЛЬЗОВАТЕЛЕЙ
# -------------------------

USERS_FILE = "users.json"

if os.path.exists(USERS_FILE):
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            seen_users = set(data)
        else:
            print("users.json содержит неправильный формат.")
            seen_users = set()

    except json.JSONDecodeError:
        print("users.json пустой или повреждён. Создаём новую базу.")
        seen_users = set()

else:
    seen_users = set()


def save_users():
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            list(seen_users),
            f,
            ensure_ascii=False,
            indent=2
        )


# -------------------------
# 📩 ОБРАБОТЧИК
# -------------------------

@client.on(events.NewMessage(chats=source_chats))
async def handler(event):

    try:
        sender = await event.get_sender()

    except ChannelPrivateError:
        print("Нет доступа к каналу")
        return

    except Exception as e:
        print(f"Ошибка sender: {e}")
        return

    # 🔥 только реальные пользователи
    if not sender or sender.__class__.__name__ != "User":
        return

    first_name = getattr(sender, "first_name", "")
    username = getattr(sender, "username", None)
    user_id = sender.id

    # 🚫 если нет username — пропуск
    if not username:
        return

    # 🚫 уже был
    if user_id in seen_users:
        return

    # 🔥 тип сообщения
    if event.photo:
        text = "(фото)"

    elif event.video:
        text = "(видео)"

    elif event.voice:
        text = "(голосовое)"

    elif event.document:
        text = "(файл)"

    elif event.sticker:
        text = "(стикер)"

    else:
        text = event.raw_text or "(пустое сообщение)"

    try:
        chat = await event.get_chat()
        chat_title = getattr(chat, "title", "ЛС")

    except Exception:
        chat_title = "Неизвестно"

    user_mention = f"@{username}"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✉️ Написать",
                    url=f"https://t.me/{username}"
                )
            ]
        ]
    )

    message = (
        f"🔥 Новый пользователь\n\n"
        f"Чат: {chat_title}\n"
        f"Имя: {first_name}\n"
        f"Пользователь: {user_mention}\n"
        f"ID: {user_id}\n\n"
        f"Текст:\n{text}"
    )

    try:
        await bot.send_message(
            receiver_chat_id,
            message,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

        # Добавляем пользователя в базу ТОЛЬКО после успешной отправки
        seen_users.add(user_id)
        save_users()

        print(f"Новый пользователь: {username} ({user_id})")

    except Exception as e:
        print(f"Ошибка отправки: {e}")


# -------------------------
# 🚀 ЗАПУСК
# -------------------------

async def main():
    print("Парсер запущен...")
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())