from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import pandas as pd
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Константы
SCHEDULE_FILE = 'schedule.xlsx'
WEEKDAYS = {
    'Monday': 'Понедельник',
    'Tuesday': 'Вторник',
    'Wednesday': 'Среда',
    'Thursday': 'Четверг',
    'Friday': 'Пятница',
    'Saturday': 'Суббота',
    'Sunday': 'Воскресенье'
}

# Функция для получения расписания на конкретный день
def get_schedule_for_day(day):
    try:
        df = pd.read_excel(SCHEDULE_FILE, header=0)
        day = day.title()

        if day in df['Дни недели'].values:
            schedule = df.loc[df['Дни недели'] == day].iloc[0]
            text = f"Расписание на {day}:\n"
            for i, lesson in enumerate(schedule[1:], start=1):
                text += f"Пара {i}: {lesson}\n"
        else:
            text = f"Расписание для {day} не найдено."
    except Exception as e:
        logger.error(f"Ошибка при получении расписания: {e}")
        text = "Произошла ошибка при получении расписания."
    
    return text

# Функция для получения расписания на всю неделю
def get_schedule_for_week():
    try:
        df = pd.read_excel(SCHEDULE_FILE, header=0)
        text = "Расписание на всю неделю:\n"
        for day in df['Дни недели'].values:
            schedule = df.loc[df['Дни недели'] == day].iloc[0]
            text += f"\nРасписание на {day}:\n"
            for i, lesson in enumerate(schedule[1:], start=1):
                text += f"Пара {i}: {lesson}\n"
    except Exception as e:
        logger.error(f"Ошибка при получении расписания: {e}")
        text = "Произошла ошибка при получении расписания."
    
    return text

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['День', 'Неделя']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Привет! Отправь /day, чтобы получить расписание на сегодня, или /week, чтобы получить расписание на всю неделю.', reply_markup=reply_markup)

# Обработчик команды /day
async def day_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day = datetime.now().strftime('%A')
    russian_day = WEEKDAYS.get(day, 'Понедельник')
    schedule = get_schedule_for_day(russian_day)
    await update.message.reply_text(schedule)

# Обработчик команды /week
async def week_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    schedule = get_schedule_for_week()
    await update.message.reply_text(schedule)

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == 'День':
        await day_schedule(update, context)
    elif text == 'Неделя':
        await week_schedule(update, context)

# Основная функция
def main():
    token = '7253126841:AAGodh8eqvcTWmjlweRoXjQgyYyEI3QseWg'

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('day', day_schedule))
    application.add_handler(CommandHandler('week', week_schedule))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота с использованием run_polling
    application.run_polling(timeout=30)

if __name__ == '__main__':
    main()