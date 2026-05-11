import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

# -------------------------
# 🔹 ТЕМЫ
# -------------------------

algebra_topics = {
    "stepeni": "Степени",
    "uravneniya": "Уравнения",
    "progressia": "Прогрессии",
    "teoria_v": "Теория вероятности",
    "tab_kvadratov": "Таблица квадратов",
    "fsy": "ФСУ и преобразования",
}

geometry_topics = {
    "treugolniki": "Треугольники",
    "okruzhnost": "Окружность",
    "romb": "Ромб",
    "chetirehyg": "Четырехугольники",
    "sum_mnogoyg": "Сумма углов многоугольников",
    "trigonometry": "Тригонометрия",
    "paralel_pryamie": "Признаки параллельности прямых",
}


# -------------------------
# 🔹 КНОПКИ
# -------------------------

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Алгебра", callback_data="algebra")],
        [InlineKeyboardButton(text="📐 Геометрия", callback_data="geometry")],
        [InlineKeyboardButton(text="🔢 Задания 1–5", callback_data="tasks15")]
    ])


def topics_menu(section):
    topics = algebra_topics if section == "algebra" else geometry_topics

    buttons = []

    for key, name in topics.items():
        buttons.append([
            InlineKeyboardButton(
                text=name,
                callback_data=f"{section}_{key}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(text="⬅ Назад", callback_data="main")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_topics(section):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅ К темам", callback_data=section)]
    ])


# -------------------------
# ▶️ СТАРТ
# -------------------------

@dp.message()
async def start(message: types.Message):
    await message.answer(
        "📚 Бот-памятка для ОГЭ по математике\n\n"
        "ОГЭ по алгебре в 9 классе — важный экзамен, который влияет на дальнейшее обучение. "
        "Для успешной подготовки важно не только знать теорию, но и иметь удобный справочник "
        "с основными формулами и методами решения задач.\n\n"
        "Выбери раздел:",
        reply_markup=main_menu()
    )


# -------------------------
# 🔘 ОБРАБОТКА КНОПОК
# -------------------------

@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    data = callback.data

    # главное меню
    if data == "main":
        await callback.message.edit_text(
            "📚 Выбери раздел:",
            reply_markup=main_menu()
        )

    # алгебра
    elif data == "algebra":
        await callback.message.edit_text(
            "📘 Алгебра",
            reply_markup=topics_menu("algebra")
        )

    # геометрия
    elif data == "geometry":
        await callback.message.edit_text(
            "📐 Геометрия",
            reply_markup=topics_menu("geometry")
        )

    # 🔥 ЗАДАНИЯ 1–5 (сразу отправляем ВСЕ картинки)
    elif data == "tasks15":
        folder = "images/tasks15"

        try:
            files = sorted(os.listdir(folder))

            for file in files:
                if file.endswith(".jpg") or file.endswith(".png"):
                    photo = FSInputFile(f"{folder}/{file}")
                    await callback.message.answer_photo(photo)

        except:
            await callback.message.answer("❌ Папка с заданиями не найдена")

    # тема → показать ОДНУ ИЛИ НЕСКОЛЬКО картинок
    else:
        section, topic = data.split("_", 1)
        folder = f"images/{section}/{topic}"

        try:
            files = sorted(os.listdir(folder))

            for file in files:
                if file.endswith(".jpg") or file.endswith(".png"):
                    photo = FSInputFile(f"{folder}/{file}")
                    await callback.message.answer_photo(photo)

            await callback.message.answer(
                "📌 Памятка",
                reply_markup=back_to_topics(section)
            )

        except:
            await callback.message.answer("❌ Папка или изображения не найдены")


# ------------------
# ▶️ ЗАПУСК
# -------------------------

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
