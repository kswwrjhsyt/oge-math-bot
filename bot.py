import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message, CallbackQuery
from aiogram.filters import CommandStart

# ---------------------------------
# 🔐 ТОКЕН (безопасное получение)
# ---------------------------------
try:
    from config import TOKEN
except ImportError:
    bot = Bot(token=os.getenv('BOT_TOKEN'))

if not TOKEN:
    raise ValueError("❌ Токен не найден. Добавьте переменную окружения BOT_TOKEN на сервере или создайте config.py")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# -------------------------
# 📚 ТЕМЫ
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
    "sum_mnogoyg": "Сумма углов",
    "trigonometry": "Тригонометрия",
    "paralel_pryamie": "Параллельные прямые",
}

# -------------------------
# 📄 ТЕКСТОВЫЕ ПАМЯТКИ (HTML формат)
# -------------------------
algebra_texts = {
    "stepeni": (
        "📌 <b>Степени</b>\n\n"
        "Степень показывает, сколько раз число умножается само на себя. Это удобная запись для больших чисел.\n\n"
        "⚠️ <b>Важно помнить:</b>\n"
        "• Любое число в нулевой степени равно 1 (кроме 0⁰).\n"
        "• Отрицательная степень — это дробь: <code>a⁻ⁿ = 1 / aⁿ</code>.\n"
        "• При умножении с одинаковым основанием показатели <b>складываются</b>, при делении — <b>вычитаются</b>.\n\n"
        "<i>Примеры:</i>\n"
        "✅ 2³ = 2 × 2 × 2 = 8\n"
        "✅ 5² × 5³ = 5⁵ = 3125\n"
        "✅ 7⁻² = 1 / 7² = 1 / 49"
    ),
    "uravneniya": (
        "📌 <b>Уравнения</b>\n\n"
        "Уравнение — это равенство, содержащее неизвестное (обычно x). Решить его — найти корни.\n\n"
        "⚠️ <b>Важно помнить:</b>\n"
        "• При переносе слагаемого через знак «=» его знак меняется на противоположный.\n"
        "• Квадратные уравнения (ax² + bx + c = 0) решаются через Дискриминант: <code>D = b² - 4ac</code>.\n"
        "• Если D > 0 (2 корня), D = 0 (1 корень), D < 0 (нет корней).\n\n"
        "<i>Примеры:</i>\n"
        "✅ Линейное: 3x - 6 = 0  =>  3x = 6  =>  x = 2\n"
        "✅ Квадратное: x² - 5x + 6 = 0. По теореме Виета: x₁=2, x₂=3."
    ),
    "progressia": (
        "📌 <b>Прогрессии (Задание 14)</b>\n\n"
        "Последовательности чисел, построенные по определенному правилу.\n\n"
        "⚠️ <b>Важно помнить:</b>\n"
        "• <b>Арифметическая:</b> каждое число получается прибавлением одного и того же числа (разности d).\n"
        "• <b>Геометрическая:</b> каждое число получается умножением на одно и то же число (знаменатель q).\n\n"
        "<i>Примеры:</i>\n"
        "✅ Арифметическая: 2, 5, 8, 11... (здесь d = +3). Пятый член будет 11 + 3 = 14.\n"
        "✅ Геометрическая: 3, 6, 12, 24... (здесь q = ×2)."
    ),
    "teoria_v": (
        "📌 <b>Теория вероятности</b>\n\n"
        "Шанс того, что произойдет нужное нам событие.\n\n"
        "⚠️ <b>Важно помнить:</b>\n"
        "• Формула: <code>P = (нужные исходы) / (все возможные исходы)</code>.\n"
        "• Вероятность всегда от 0 до 1. В ответ в ОГЭ записывается десятичная дробь!\n\n"
        "<i>Пример:</i>\n"
        "✅ В корзине 4 красных и 6 зеленых яблок (всего 10). Вероятность достать красное: P = 4 / 10 = 0.4."
    ),
    "tab_kvadratov": (
        "📌 <b>Таблица квадратов</b>\n\n"
        "Квадрат числа — это результат умножения числа само на себя. Выдается в справочных материалах на экзамене!\n\n"
        "⚠️ <b>Важно помнить:</b>\n"
        "• Умение быстро узнавать квадраты чисел от 11 до 20 сэкономит тебе много времени.\n"
        "• Квадратный корень — обратное действие. √144 = 12.\n\n"
        "<i>Примеры:</i>\n"
        "✅ 11² = 121, 12² = 144, 15² = 225, 20² = 400."
    ),
    "fsy": (
        "📌 <b>Формулы сокращенного умножения (ФСУ)</b>\n\n"
        "Шаблоны для быстрого раскрытия скобок или группировки множителей.\n\n"
        "⚠️ <b>Важно помнить:</b>\n"
        "• Разность квадратов: <code>a² - b² = (a - b)(a + b)</code>\n"
        "• Квадрат суммы: <code>(a + b)² = a² + 2ab + b²</code>\n"
        "• В ОГЭ они часто прячутся под корнями или в дробях для сокращения.\n\n"
        "<i>Примеры:</i>\n"
        "✅ x² - 25 = (x - 5)(x + 5)\n"
        "✅ (x + 3)² = x² + 6x + 9"
    ),
}

geometry_texts = {
    "treugolniki": (
        "📌 <b>Треугольники</b>\n\n"
        "Фигура из трёх отрезков. Основа всей геометрии.\n\n"
        "⚠️ <b>Важно помнить:</b>\n"
        "• Сумма всех углов ВСЕГДА 180°.\n"
        "• <b>Теорема Пифагора</b> (для прямоугольных): <code>c² = a² + b²</code> (квадрат гипотенузы равен сумме квадратов катетов).\n"
        "• Площадь: S = 1/2 × a × h (половина основания на высоту).\n\n"
        "<i>Пример:</i>\n"
        "✅ Если катеты 3 и 4, то гипотенуза = √(3² + 4²) = √(9+16) = √25 = 5 (Египетский треугольник)."
    ),
    "okruzhnost": (
        "📌 <b>Окружность</b>\n\n"
        "Все точки на одинаковом расстоянии от центра.\n\n"
        "⚠️ <b>Важно помнить:</b>\n"
        "• Касательная всегда перпендикулярна радиусу (образует угол 90°).\n"
        "• Центральный угол равен дуге, на которую опирается.\n"
        "• Вписанный угол равен ПОЛОВИНЕ дуги, на которую опирается.\n\n"
        "<i>Пример:</i>\n"
        "✅ Если дуга окружности равна 80°, то вписанный угол, опирающийся на нее, будет 40°."
    ),
    "romb": (
        "📌 <b>Ромб</b>\n\n"
        "Это параллелограмм, у которого все 4 стороны равны.\n\n"
        "⚠️ <b>Важно помнить:</b>\n"
        "• Диагонали ромба пересекаются под прямым углом (90°).\n"
        "• Диагонали являются биссектрисами его углов.\n"
        "• Площадь: S = (d₁ × d₂) / 2.\n\n"
        "<i>Пример:</i>\n"
        "✅ Если диагонали ромба 6 и 8, его площадь = (6 × 8) / 2 = 24."
    ),
    "chetirehyg": (
        "📌 <b>Четырёхугольники</b>\n\n"
        "Трапеции, параллелограммы, квадраты, прямоугольники.\n\n"
        "⚠️ <b>Важно помнить:</b>\n"
        "• Сумма углов любого четырёхугольника = 360°.\n"
        "• Площадь параллелограмма: S = a × h.\n"
        "• Площадь трапеции: полусумма оснований умножить на высоту <code>S = (a+b)/2 × h</code>.\n\n"
        "<i>Пример:</i>\n"
        "✅ В трапеции основания 4 и 10, высота 5. Площадь = ((4+10)/2) × 5 = 7 × 5 = 35."
    ),
    "sum_mnogoyg": (
        "📌 <b>Сумма углов многоугольника</b>\n\n"
        "Как посчитать все внутренние углы в любой фигуре.\n\n"
        "⚠️ <b>Важно помнить:</b>\n"
        "• Формула: <code>(n - 2) × 180°</code>, где n — количество углов (сторон).\n\n"
        "<i>Примеры:</i>\n"
        "✅ Для треугольника (n=3): (3-2) × 180 = 180°.\n"
        "✅ Для пятиугольника (n=5): (5-2) × 180 = 3 × 180 = 540°."
    ),
    "trigonometry": (
        "📌 <b>Тригонометрия</b>\n\n"
        "Отношения сторон в прямоугольном треугольнике.\n\n"
        "⚠️ <b>Важно помнить:</b>\n"
        "• <b>Синус (sin)</b> = противолежащий катет / гипотенуза.\n"
        "• <b>Косинус (cos)</b> = прилежащий катет / гипотенуза.\n"
        "• <b>Тангенс (tg)</b> = противолежащий / прилежащий.\n\n"
        "<i>Пример:</i>\n"
        "✅ Катеты 3 и 4, гипотенуза 5. Синус угла напротив катета 3 равен 3/5 = 0.6."
    ),
    "paralel_pryamie": (
        "📌 <b>Параллельные прямые</b>\n\n"
        "Прямые, которые никогда не пересекаются.\n\n"
        "⚠️ <b>Важно помнить (при пересечении секущей):</b>\n"
        "• Накрест лежащие углы РАВНЫ (образуют букву Z).\n"
        "• Соответственные углы РАВНЫ (похожи на ступеньки).\n"
        "• Односторонние углы в сумме дают 180°.\n\n"
        "<i>Пример:</i>\n"
        "✅ Если один из накрест лежащих углов равен 45°, то второй тоже равен 45°."
    ),
}

# -------------------------
# 🔘 КЛАВИАТУРЫ
# -------------------------
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Алгебра", callback_data="algebra")],
        [InlineKeyboardButton(text="📐 Геометрия", callback_data="geometry")],
        [InlineKeyboardButton(text="🔢 Задания 1–5", callback_data="tasks15")]
    ])

def topics_menu(section):
    topics = algebra_topics if section == "algebra" else geometry_topics
    buttons = [[InlineKeyboardButton(text=name, callback_data=f"{section}_{key}")] for key, name in topics.items()]
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_to_topics(section):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ К темам", callback_data=section)]
    ])

# -------------------------
# 🧠 ОТПРАВКА ТЕМЫ (картинки + текст)
# -------------------------
async def send_topic(callback: CallbackQuery, section: str, topic_key: str):
    folder = os.path.join("images", section, topic_key)
    text_dict = algebra_texts if section == "algebra" else geometry_texts
    explanation = text_dict.get(topic_key, "✅ Материал подготовлен. Изучи картинки выше.")

    # Отправляем картинки из папки
    if os.path.exists(folder):
        files = sorted(os.listdir(folder))
        for file in files:
            if file.lower().endswith((".jpg", ".png", ".jpeg")):
                try:
                    photo = FSInputFile(os.path.join(folder, file))
                    await callback.message.answer_photo(photo)
                except Exception as e:
                    logger.error(f"Ошибка отправки {file}: {e}")
    else:
        await callback.message.answer("❌ Папка с картинками не найдена. Создайте папку: " + folder)

    # Отправляем текстовое объяснение
    await callback.message.answer(explanation, parse_mode="HTML", reply_markup=back_to_topics(section))

# -------------------------
# ▶️ СТАРТ
# -------------------------
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "📚 <b>Бот-памятка для ОГЭ по математике</b>\n\n"
        "Привет! Я помогу тебе освежить знания. Выбери нужный раздел ниже:",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

# -------------------------
# 🔘 ОБРАБОТКА КНОПОК
# -------------------------
@dp.callback_query()
async def callbacks(callback: CallbackQuery):
    data = callback.data
    logger.info(f"Нажата кнопка: {data}")

    if data == "main":
        await callback.message.edit_text("📚 <b>Выбери раздел:</b>", parse_mode="HTML", reply_markup=main_menu())
    elif data == "algebra":
        await callback.message.edit_text("📘 <b>Алгебра</b>", parse_mode="HTML", reply_markup=topics_menu("algebra"))
    elif data == "geometry":
        await callback.message.edit_text("📐 <b>Геометрия</b>", parse_mode="HTML", reply_markup=topics_menu("geometry"))
    elif data == "tasks15":
        folder = "images/tasks15"
        if os.path.exists(folder):
            files = sorted(os.listdir(folder))
            for file in files:
                if file.lower().endswith((".jpg", ".png", ".jpeg")):
                    try:
                        photo = FSInputFile(os.path.join(folder, file))
                        await callback.message.answer_photo(photo)
                    except Exception as e:
                        logger.error(f"Ошибка отправки {file}: {e}")
        else:
            await callback.message.answer("❌ Папка с заданиями 1–5 не найдена.")
    elif "_" in data:
        section, topic = data.split("_", 1)
        await send_topic(callback, section, topic)
    else:
        await callback.message.answer("Неизвестная команда", reply_markup=main_menu())

    await callback.answer()

# -------------------------
# 🚀 ЗАПУСК
# -------------------------
async def main():
    logger.info("Бот запущен")
    # Удаляем вебхуки (на случай, если они были) и запускаем поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())