from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""مرحباً {msg.from_user.mention},
**مرحبا بك في بوت استخراج جلسات**
يمكنك استخراج جلسة بايروجرام او تيرمكس عبر البوت 
| استعمل الازرار في الاسفل |""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=" ‹ استخراج ›", callback_data="generate")
                ],
                [
                    InlineKeyboardButton("‹ سورس سبارك ›️", url="https://t.me/ZZZ7iZ"),
                    InlineKeyboardButton("‹ مطور البوت ›", user_id=5012406813)
                ]
            ]
        ),
        disable_web_page_preview=True,
    )
