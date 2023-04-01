import os
from dotenv import load_dotenv
from telegram.ext import *
from telegram import ParseMode
import responses
import mining_data
import data
import datetime
import time
import pytz

# https://stackoverflow.com/questions/62289341/telegram-bot-api-python-run-daily-method
# https://docs.python-telegram-bot.org/en/stable/telegram.ext.jobqueue.html
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#message-formatting-bold-italic-code-

load_dotenv()
bot_token = os.environ.get('PKT_MINING_BOT_TOKEN')
updater = Updater(token=bot_token, use_context=True)

def mining_data_message(context):
    chat_id = context.job.context
    addresses = data.get_addresses(chat_id)
    message = mining_data.get_mining_data(addresses)
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)

def queue_daily_message(chat_id, hour, minute, timezone):
    message_time = datetime.time(hour=hour, minute=minute, tzinfo=pytz.timezone(timezone))
    updater.job_queue.run_daily(mining_data_message, message_time, days=(0, 1, 2, 3, 4, 5, 6), context=chat_id, name=str(chat_id))

def restore_subscriptions():
    chat_ids = data.get_subscribed_chat_ids()
    count = len(chat_ids)
    if count > 0:
        for chat_id in chat_ids:
            chat_id = chat_id[0]
            user_time_str = data.get_time(chat_id)
            user_time = datetime.datetime.strptime(user_time_str, "%H:%M")
            user_hour = user_time.hour
            user_minute = user_time.minute
            user_timezone = str(data.get_timezone(chat_id))
            queue_daily_message(chat_id, user_hour, user_minute, user_timezone)
    print("Number of subscriptions restored: " + str(count))

def start_command(update, context):
    update.message.reply_text("Thanks for taking the time to try this bot. Use /help to see all the available commands.")

def subscribe_command(update, context):
    chat_id = update.message.chat_id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    
    if len(current_jobs) == 1:
        for job in current_jobs:
            job.schedule_removal() # Kill the existing job first
        result = "Subscription updated."
    else:
        result = "Subscription started."
    
    user_time_str = data.get_time(chat_id)
    user_time = datetime.datetime.strptime(user_time_str, "%H:%M")
    user_hour = user_time.hour
    user_minute = user_time.minute
    user_timezone = str(data.get_timezone(chat_id))

    queue_daily_message(chat_id, user_hour, user_minute, user_timezone)
    data.set_subscription(chat_id, "1")

    # Send a message every hour:
    #context.job_queue.run_repeating(mining_data_message, interval=3600, first=1, context=update.message.chat_id)

    result += " Your daily message will be sent every day at " + user_time_str + " in the " + user_timezone + " timezone."
    update.message.reply_text(result)

def stop_command(update, context):
    chat_id = update.message.chat_id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))

    if len(current_jobs) == 0:
        result = "No subscription is running."
    else:
        for job in current_jobs:
            job.schedule_removal()
        data.set_subscription(chat_id, "0")
        result = "Subscription stopped."
    update.message.reply_text(result)

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

def help_command(update, context):
    update.message.reply_text("""Available commands:\n
/start Displays a welcome message.
/add_address <address> Adds a PKT address to your list.
/remove_address <address> Removes a PKT address from your list.
/list_addresses View the PKT addresses on your list.
/set_time <time> Set the time of the subscription message.
/set_timezone <timezone> Set the timezone for the time of the message.
/subscribe Start/update the subscription.
/stop Stop the subscription.
/help Shows this list.""")

#def check_command(update, context: CallbackContext):
#    update.message.reply_text(f"Check: {context.bot.base_url}")

def handle_message(update, context):
    message = update.message.text
    response = responses.sample_responses(message)
    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}.")

def main():

    data.create_tables()

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("subscribe", subscribe_command))
    dp.add_handler(CommandHandler("stop", stop_command))
    dp.add_handler(CommandHandler("list_addresses", list_addresses_command))
    dp.add_handler(CommandHandler("add_address", add_address_command))
    dp.add_handler(CommandHandler("remove_address", remove_address_command))
    dp.add_handler(CommandHandler("set_time", set_time_command))
    dp.add_handler(CommandHandler("set_timezone", set_timezone_command))
    dp.add_handler(CommandHandler("help", help_command))
    #dp.add_handler(CommandHandler("check", check_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    #updater.bot.send_message(767344183, text='Howdy')
    #queue_daily_message(767344183, 19, 38, "Europe/Amsterdam")
    restore_subscriptions()

    updater.start_polling()

    print ("PKT Mining Monitor bot started.")

    updater.idle()

main()