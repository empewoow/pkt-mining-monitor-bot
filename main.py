import constants
from telegram.ext import *
from telegram import ParseMode
import responses
import miner_info
import data
import datetime
import time
import pytz

# https://stackoverflow.com/questions/62289341/telegram-bot-api-python-run-daily-method
# https://docs.python-telegram-bot.org/en/stable/telegram.ext.jobqueue.html
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#message-formatting-bold-italic-code-

def start_command(update, context):

    chat_id = update.message.chat_id
    user_time_str = data.get_time(chat_id)
    user_time = datetime.datetime.strptime(user_time_str, "%H:%M")
    user_hour = user_time.hour
    user_minute = user_time.minute
    user_timezone = str(data.get_timezone(chat_id))

    # Send the daily message at the preferred time of the user:
    message_time = datetime.time(hour=user_hour, minute=user_minute, tzinfo=pytz.timezone(user_timezone))
    context.job_queue.run_daily(daily_message, message_time, days=(0, 1, 2, 3, 4, 5, 6), context=update.message.chat_id)

    # Send a message every hour:
    #context.job_queue.run_repeating(callback_message, interval=3600, first=1, context=update.message.chat_id)

    update.message.reply_text("Subscription started. Your daily message will be sent every day at " + user_time_str + " in the " + user_timezone + " timezone.")

def callback_message(context):
    chat_id = context.job.context    
    addresses = data.get_addresses(chat_id)
    message = miner_info.get_miner_info(addresses)
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)

def daily_message(context):
    chat_id = context.job.context
    addresses = data.get_addresses(chat_id)
    message = miner_info.get_miner_info(addresses)
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)

def list_addresses_command(update, context):
    chat_id = update.message.chat_id
    message = update.message.text
    result = data.list_addresses(chat_id, message)
    update.message.reply_text(result)

def add_address_command(update, context):
    chat_id = update.message.chat_id
    message = update.message.text
    result = data.add_address(chat_id, message)
    update.message.reply_text(result)

def remove_address_command(update, context):
    chat_id = update.message.chat_id
    message = update.message.text
    result = data.remove_address(chat_id, message)
    update.message.reply_text(result)

def set_time_command(update, context):
    chat_id = update.message.chat_id
    message = update.message.text
    result = data.set_time(chat_id, message)
    update.message.reply_text(result)

def set_timezone_command(update, context):
    chat_id = update.message.chat_id
    message = update.message.text
    result = data.set_timezone(chat_id, message)
    update.message.reply_text(result)

#def check_command(update, context: CallbackContext):
#    update.message.reply_text(f"Check: {context.bot.base_url}")

def help_command(update, context):
    update.message.reply_text("""Available commands:\n
/add_address Adds a PKT address to your list.
/remove_address Removes a PKT address from your list.
/list_addresses View the PKT addresses on your list.
/set_time Set the time of the subscription message.
/set_timezone Set the timezone for the time of the message.
/start Start the subscription.
/help Shows this list.""")

def handle_message(update, context):
    message = update.message.text
    response = responses.sample_responses(message)
    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}.")

def main():

    data.create_table()

    updater = Updater(constants.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("list_addresses", list_addresses_command))
    dp.add_handler(CommandHandler("add_address", add_address_command))
    dp.add_handler(CommandHandler("remove_address", remove_address_command))
    dp.add_handler(CommandHandler("set_time", set_time_command))
    dp.add_handler(CommandHandler("set_timezone", set_timezone_command))
    #dp.add_handler(CommandHandler("check", check_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()

    print ("PKT Miner Monitor bot started.")

    updater.idle()

main()