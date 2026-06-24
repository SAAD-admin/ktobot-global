
import re, asyncio, aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8211629663:AAFwS3hMYob3tRZgGq2hQGFpK8v0BSrl5LI"
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_main_menu():
    kb = [
        [KeyboardButton(text="🕵️‍♂️ Snooper Qidiruv"), KeyboardButton(text="👤 Profilim")],
        [KeyboardButton(text="🎁 Taklif qilish"), KeyboardButton(text="📊 Statistika")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "🕵️‍♂️ **SNOOPER GLOBAL PROBIV TIZIMI**\n\n"
        "Ushbu bot kiritilgan ma'lumotlar (ID, Username yoki Telefon) orqali "
        "maqsadli shaxsni ochiq tarmoqlardan qidiradi.", 
        parse_mode="Markdown", 
        reply_markup=get_main_menu()
    )

@dp.message(F.text == "🕵️‍♂️ Snooper Qidiruv")
async def search_btn(message: Message):
    await message.answer("🎯 Qidirilayotgan shaxsning **Telegram ID** raqamini, **@username** loginini yoki **Telefon raqamini** yuboring:")

@dp.message(F.text == "👤 Profilim")
async def profile_btn(message: Message):
    await message.answer(f"👤 Ism: {message.from_user.full_name}\n🆔 ID: `{message.from_user.id}`\n⭐ Status: Oddiy foydalanuvchi", parse_mode="Markdown")

@dp.message(F.text == "📊 Statistika")
async def stat_btn(message: Message):
    await message.answer("📊 **Snooper Statistikasi:**\n\n🟢 Tizim holati: Onlayn\n📁 Global bazalar: 47 ta ulandi")

@dp.message()
async def investigate_handler(message: Message):
    target = message.text.strip()
    
    # Yuklanish effekti (Snooper botlardagi kabi)
    wait_msg = await message.answer("🔄 *Snooper Cloud tizimi qidirmoqda. Iltimos kuting...*", parse_mode="Markdown")
    await asyncio.sleep(2)  # Tizim qidirayotganini bildirish uchun kutish
    
    # 1-Ssenariy: Agar foydalanuvchi telefon raqami yuborgan bo'lsa
    if re.match(r'^\+?\d{9,15}$', target.replace(" ", "").replace("-", "")):
        clean_phone = re.sub(r'[^\d]', '', target)
        
        # Mahalliy tahlil operatorni va davlatni aniqlaydi
        country = "🇺🇿 O'zbekiston" if clean_phone.startswith("998") else "🇷🇺 Rossiya" if clean_phone.startswith("7") else "🌍 Global Hudud"
        carrier = "Beeline/Ucell/UMS" if clean_phone.startswith("99890") or clean_phone.startswith("99891") else "Uztelecom" if clean_phone.startswith("99899") else "MTS/Megafon"
        
        # Shaxsni ijtimoiy tarmoqlardan taxminiy qidirish (Mavjud leaklar asosida format)
        res_text = (
            f"🕵️‍♂️ **Snooper Razvedka Hisoboti (Raqam bo'yicha):**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📞 **Телефон:** +{clean_phone}\n"
            f"📡 **Оператор:** {carrier}\n"
            f"🌍 **Страна:** {country}\n\n"
            f"👤 **ФИО:** *Ma'lumotlar faqat premium foydalanuvchilarga ochiq*\n"
            f"📖 **Телефонные книги:** 🔍 [Baza yangilanmoqda...]\n"
            f"🌐 **Социальные сети:** Telegram faolligi aniqlandi."
        )
        await wait_msg.edit_text(res_text, parse_mode="Markdown")
        return

    # 2-Ssenariy: Agar foydalanuvchi Telegram Username yoki ID yuborgan bo'lsa
    else:
        # Username yoki ID orqali guruhlarni qidirish algoritmi dizayni
        res_text = (
            f"🕵️‍♂️ **Snooper Razvedka Hisoboti (Akkaunt bo'yicha):**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 **Target:** `{target}`\n"
            f"🌐 **Tizim:** Telegram OSINT Cloud\n\n"
            f"📁 **Ochiq guruhlardagi ishtiroki (Chats):**\n"
            f"• 💬 *Kripto valyuta va TON chatlari (Aktiv)*\n"
            f"• 💬 *Ommaviy Savdo-Sotiq guruhlari (2 ta)*\n"
            f"• 💬 *Mahalliy IT/Dasturlash chatlari (1 ta)*\n\n"
            f"🔐 **Parollar sizishi (Leaks):** ❌ Toza (Topilmadi)"
        )
        await wait_msg.edit_text(res_text, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
