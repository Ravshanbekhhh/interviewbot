import asyncio
import json
import random
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

# -------------------------
TOKEN = "8401846824:AAHMmF5-nzZbBFXc53tcoh9u1pqCvY8cPrg"
ADMIN_ID = 7485738561
# -------------------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

DATA_FILE = "questions.json"

# Savollarni JSON dan o‘qish
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Savollarni JSON ga yozish
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Start menu
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎯 Savol olish")],
        [KeyboardButton(text="📂 Kategoriyalar bo‘yicha (tezkunda)")]
    ],
    resize_keyboard=True
)


# ----------- START ------------
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("👋 Salom! Men dasturlash intervyu savollari botiman.\nQuyidagilardan birini tanlang:", reply_markup=start_kb)

@dp.message(Command("help"))
async def start_cmd(message: Message):
    await message.answer("Bu bot sizni it boyicha savol javob qilib tekshiradi")


# ----------- SAVOL OLISH ------------
@dp.message(F.text == "🎯 Savol olish")
async def random_question(message: Message):
    data = load_data()
    if not data:
        await message.answer("❌ Savollar hali qo‘shilmagan.")
        return

    q = random.choice(data)
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Javobni ko‘rish", callback_data=f"answer_{q['id']}")]
    ])
    await message.answer(f"❓ Savol:\n{q['question']}", reply_markup=inline_kb)


# ----------- JAVOB KO‘RISH ------------
@dp.callback_query(F.data.startswith("answer_"))
async def show_answer(callback: CallbackQuery):
    q_id = int(callback.data.split("_")[1])
    data = load_data()

    for q in data:
        if q["id"] == q_id:
            await callback.message.answer(f"💡 Javob:\n{q['answer']}")
            break
    await callback.answer()


# ----------- ADMIN PANEL ------------
@dp.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Siz admin emassiz!")
        return

    await message.answer("🔐 Admin panel:\nSavol qo‘shish uchun quyidagi formatda yozing:\n\nsavol || javob")


# ----------- ADMIN YANGI SAVOL QO‘SHISH ------------
@dp.message(F.text.contains("||"))
async def add_question(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        q_text, a_text = message.text.split("||")
        q_text, a_text = q_text.strip(), a_text.strip()

        data = load_data()
        new_id = max([q["id"] for q in data], default=0) + 1

        new_q = {"id": new_id, "question": q_text, "answer": a_text}
        data.append(new_q)
        save_data(data)

        await message.answer("✅ Savol va javob qo‘shildi!")
    except:
        await message.answer("❌ Xatolik! Format: savol || javob bo‘lishi kerak.")


# -------------------------
async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
