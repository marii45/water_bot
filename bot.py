import time
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

TOKEN = '7778834611:AAE0Qat6xNmQiKRxdQxt1GV1QOEFmZY0S7M'
MSG = "Did you drink enough water today, {}? "

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

# Mapping of user reminders in seconds
user_intervals = {}

# Interval options in seconds
INTERVALS = {
    'daily': 86400,         # 24 hours
    'every_3_days': 259200, # 3 days
    'weekly': 604800        # 7 days
}

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_fullname = message.from_user.full_name

    # Log user details
    logging.info(f'{user_id} {user_fullname} {time.asctime()}')

    # Prompt user to set reminder frequency
    await message.reply(
        f"Hello, {user_fullname}. How often would you like to receive water reminders?\n"
        "Use one of the following commands:\n"
        "`/set_daily` - Once a day\n"
        "`/set_every3days` - Every 3 days\n"
        "`/set_weekly` - Once a week",
        parse_mode="Markdown"
    )

@dp.message_handler(commands=['set_daily', 'set_every3days', 'set_weekly'])
async def set_frequency_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # Determine the interval based on command
    if message.text == '/set_daily':
        interval = INTERVALS['daily']
        interval_name = "once a day"
    elif message.text == '/set_every3days':
        interval = INTERVALS['every_3_days']
        interval_name = "every 3 days"
    elif message.text == '/set_weekly':
        interval = INTERVALS['weekly']
        interval_name = "once a week"
    
    # Store the interval and start reminders
    user_intervals[user_id] = interval
    await message.reply(f"Reminder set! You'll receive reminders {interval_name}.")
    await send_reminders(user_id, user_name, interval)

async def send_reminders(user_id, user_name, interval):
    while user_id in user_intervals and user_intervals[user_id] == interval:
        await bot.send_message(user_id, MSG.format(user_name))
        await asyncio.sleep(interval)

if __name__ == '__main__':
    executor.start_polling(dp)
