from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from pyrogram1 import Client as Client1
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram1.errors import (
    ApiIdInvalid as ApiIdInvalid1,
    PhoneNumberInvalid as PhoneNumberInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1,
    PhoneCodeExpired as PhoneCodeExpired1,
    SessionPasswordNeeded as SessionPasswordNeeded1,
    PasswordHashInvalid as PasswordHashInvalid1
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config



ask_ques = "**اضغط لبدا استخراج جلسة**"
buttons_ques = [
    [
        InlineKeyboardButton("‹ بايروجرام ›", callback_data="pyrogram1"),
        InlineKeyboardButton("‹ بايروجرام V2 ›", callback_data="pyrogram"),
    ],
    [
        InlineKeyboardButton("‹ تيرمكس ›", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("‹ بـوت بايروجرام ›", callback_data="pyrogram_bot"),
        InlineKeyboardButton(" ‹ بـوت تليثون ›", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="  اضغط لبدا استخراج كود ", callback_data="generate")
    ]
]




@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro: bool = False, is_bot: bool = False):
    if telethon:
        ty = "تيرمكس"
    else:
        ty = "بايروجرام"
        if not old_pyro:
            ty += " ᴠ2"
    if is_bot:
        ty += " ʙᴏᴛ"
    await msg.reply(f"» ¦ بـدء إنـشـاء جـلسـة **{ty}** ...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "** قم بإرسال API_ID**", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**قم بإرسال API_HASH**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "**قم بإرسال API_HASH**", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "**قم بإرسال رقم الهاتف مع مفتاح الدولة مثال+964000000**"
    else:
        t = "ارسل الان **توكن بوت** استخرجه من هنا @BotFather\ مثال : `5432198765:abcdanonymousterabaaplol`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply(" لـحظـه سـوف نـرسـل كـود لحسابـك بالتليجـرام.")
    else:
        await msg.reply("» هناك محاوله غير صحيحه")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        await msg.reply("» خطا **ᴀᴩɪ_ɪᴅ** و **ᴀᴩɪ_ʜᴀsʜ** هذا محذوف  \n\nقم ب اعادة تشغيل البوت واستخرج جلسه اخرى", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        await msg.reply("» خطا **الرقم** ليس له وجود\n\nابده من جديد وارسل رقم الهاتف صحيح", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "**قم بإرسال رمز التحقق الذي اُرسل للحساب بالشكل التالي\n\n مثال:  1 2 8 3 9**", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("**وصلت الى الحد الاقصى من الانتضار قم باعادة محاولة الاستخراج من جديد", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
            await msg.reply(" الكود خاطء **تأكد قبل الارسال**\n\nقم ب اعادة تشغيل البوت لاستخراج جلسه مره اخرى", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
            await msg.reply("** الكود انتهى اعد المحاوله لاحقا**", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
            try:
                two_step_msg = await bot.ask(user_id, "**التحقق بخطوتين مفعل لحسابك ارسل كلمة المرور لإتمام الاستخراج** ", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply(" انتهى الوقت 5دقائق\n\nانتهت المده قم ب عادة تشغيل البوت", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
                await two_step_msg.reply("** الحقق غير صحيح** ", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**تم الاستخراج ** {ty}  \n\n`{string_session}` \n\n** تم الاستخرج ياصديقي** \n\n [𝙎𝙊𝙐𝙍𝘾𝙀 𝙎𝙋𝘼𝙍𝙆](https://t.me/ZZZ7iZ)"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "تم استخراج الجلسه بنجاح ️شوف الرسائل المحفوظه {} ".format("تيرمكس" if telethon else "بايروجرام"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("** تم انهاء آلعمـليه**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("** تم اعادة تشغيل البوت**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("** تم انهاء العمليه**", quote=True)
        return True
    else:
        return False
