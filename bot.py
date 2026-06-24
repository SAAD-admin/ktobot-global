import sqlite3, re, asyncio, aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8211629663:AAFwS3hMYob3tRZgGq2hQGFpK8v0BSrl5LI"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_main_menu():
    kb = [
        [KeyboardButton(text="🔍 Raqam qidirish"), KeyboardButton(text="👤 Profilim")],
        [KeyboardButton(text="🎁 Taklif qilish"), KeyboardButton(text="📊 Statistika")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("👋 Xush kelibsiz! Raqam qidirish uchun quyidagi tugmalardan foydalaning.", reply_markup=get_main_menu())

@dp.message(F.text == "🔍 Raqam qidirish")
async def search_btn(message: Message):
    await message.answer("📱 Raqamni xalqaro formatda yuboring.\nMisol: +998901234567")

@dp.message(F.text == "👤 Profilim")
async def profile_btn(message: Message):
    await message.answer(f"👤 Ism: {message.from_user.full_name}\n🆔 ID: `{message.from_user.id}`", parse_mode="Markdown")

@dp.message(F.text == "📊 Statistika")
async def stat_btn(message: Message):
    await message.answer("📊 Bot xizmati 24/7 aktiv rejimda!")

@dp.message()
async def ordinary_msg(message: Message):
    text = message.text.strip().replace(" ", "").replace("-", "")
    phone = re.sub(r'[^\d+]', '', text)
    if not re.match(r'^\+?\d{9,15}$', phone):
        await message.answer("❌ Iltimos, to'g'ri telefon raqami yuboring.")
        return
    clean_phone = phone.replace("+", "")
    res = f"▪️ **Телефон:** +{clean_phone}\n▪️ **Оператор:** 📡 Aniqlanmoqda\n▪️ **Страна:** 🌍 Qidirilmoqda...\n\n👤 **ФИО:** ℹ️ *Baza ulanmagan*"
    await message.answer(res, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
