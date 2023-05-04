import sqlite3
import time
import pytz

# https://github.com/J4NN0/j4nn0-b0t/blob/master/util/reminder.py
# https://stackoverflow.com/questions/1322464/python-time-format-check
# https://stackoverflow.com/questions/39608283/using-python-dateutil-how-to-judge-a-timezone-string-is-valid-or-not

database_name = "data.db"

def create_tables():

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS addresses (chat_id INTEGER, address TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS settings (chat_id INTEGER, subscription INTEGER, timezone TEXT, time TEXT)")

    connection.commit()
    connection.close()

def list_addresses(chat_id, message):
    
    strings = message.split()

    if len(strings) != 1:
        return "Syntax error. Use /help for more info."
    else:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        
        rows = cursor.execute("SELECT address FROM addresses WHERE chat_id='" + str(chat_id) + "'").fetchall()

        connection.close()

        if len(rows) == 0:
            return "No PKT addresses yet!"
        else:
            addresses = ""
            for row in rows:
                addresses += str(row[0]) + "\n"
            return "Your PKT addresses:\n" + addresses

def add_address(chat_id, message):

    strings = message.split()

    if len(strings) != 2:
        return "Syntax error. Use /help for more info."
    else:
        address = strings[1]

        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        check_this_address = cursor.execute("SELECT * FROM addresses WHERE chat_id='" + str(chat_id) + "' AND address='" + address + "'").fetchall()
        address_count = cursor.execute("SELECT * FROM addresses WHERE chat_id='" + str(chat_id) + "'").fetchall()

        if len(check_this_address) == 1:
            result = "You have already added this PKT address!"
        elif len(address_count) == 5:
            result = "You cannot add more than 5 PKT addresses."
        else:
            cursor.execute("INSERT INTO addresses VALUES ('" + str(chat_id) + "', '" + address + "')")
            result = "PKT address " + address + " added!"

        connection.commit()
        connection.close()

        return result

def remove_address(chat_id, message):

    strings = message.split()

    if len(strings) != 2:
        return "Syntax error. Use /help for more info."
    else:
        address = strings[1]

        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        check_this_address = cursor.execute("SELECT * FROM addresses WHERE chat_id='" + str(chat_id) + "' AND address='" + address + "'").fetchall()
        
        if len(check_this_address) == 0:
            result = "This PKT address is not in your list."
        else:
            cursor.execute("DELETE FROM addresses WHERE chat_id='" + str(chat_id) + "' AND address='" + address + "'")
            result = "PKT address " + address + " removed..."

        connection.commit()
        connection.close()

        return result

def get_addresses(chat_id):

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    
    rows = cursor.execute("SELECT address FROM addresses WHERE chat_id='" + str(chat_id) + "'").fetchall()

    connection.close()

    return rows

def is_time_format(input):
    try:
        time.strptime(input, "%H:%M")
        return True
    except ValueError:
        return False

def set_time(chat_id, message):

    strings = message.split()

    if len(strings) != 2:
        return "Syntax error. Use /help for more info."
    else:
        time_str = strings[1]

        if not is_time_format(time_str):
            result = "This is not a valid time."
        else:

            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()

            check = cursor.execute("SELECT * FROM settings WHERE chat_id='" + str(chat_id) + "'").fetchall()

            if len(check) == 1:
                cursor.execute("UPDATE settings SET time = '" + time_str + "' WHERE chat_id='" + str(chat_id) + "'")
            else:
                cursor.execute("INSERT INTO settings VALUES ('" + str(chat_id) + "', '', '', '" + time_str + "')")

            result = "Your preferred time was set! (You may want to run /subscribe again to update the subscription.)"

            connection.commit()
            connection.close()

        return result

def set_timezone(chat_id, message):

    strings = message.split()

    if len(strings) != 2:
        return "Syntax error. Use /help for more info."
    else:
        timezone = strings[1]

        if not timezone in pytz.all_timezones:
            result = "This is not a valid timezone."
        else:

            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()

            check = cursor.execute("SELECT * FROM settings WHERE chat_id='" + str(chat_id) + "'").fetchall()

            if len(check) == 1:
                cursor.execute("UPDATE settings SET timezone = '" + timezone + "' WHERE chat_id='" + str(chat_id) + "'")
            else:
                cursor.execute("INSERT INTO settings VALUES ('" + str(chat_id) + "', '', '" + timezone + "', '')")

            result = "Your preferred timezone was set! (You may want to run /subscribe again to update the subscription.)"

            connection.commit()
            connection.close()

        return result

def get_time(chat_id):

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    rows = cursor.execute("SELECT time FROM settings WHERE chat_id='" + str(chat_id) + "'").fetchall()

    connection.close()

    default_time = "9:30" # Return something by default

    if len(rows) == 0:
        return default_time
    else:
        user_time = rows[0][0]
        if user_time == "":
            return default_time
        else:
            return user_time

def get_timezone(chat_id):

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    rows = cursor.execute("SELECT timezone FROM settings WHERE chat_id='" + str(chat_id) + "'").fetchall()

    connection.close()

    default_timezone = "Europe/Amsterdam" # Return something by default

    if len(rows) == 0:
        return default_timezone
    else:
        user_timezone = rows[0][0]
        if user_timezone == "":
            return default_timezone
        else:
            return user_timezone

def set_subscription(chat_id, subscription):

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    check = cursor.execute("SELECT * FROM settings WHERE chat_id='" + str(chat_id) + "'").fetchall()

    if len(check) == 1:
        cursor.execute("UPDATE settings SET subscription = '" + subscription + "' WHERE chat_id='" + str(chat_id) + "'")
    else:
        cursor.execute("INSERT INTO settings VALUES ('" + str(chat_id) + "', '1', '', '')")

    connection.commit()
    connection.close()

def get_subscription(chat_id):

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    rows = cursor.execute("SELECT subscription FROM settings WHERE chat_id='" + str(chat_id) + "'").fetchall()

    connection.close()

    user_subscription = rows[0][0]

    if len(rows) == 0 or user_subscription == "":
        return 0 # Return something by default
    else:
        return user_subscription

def get_subscribed_chat_ids():

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    
    rows = cursor.execute("SELECT chat_id FROM settings WHERE subscription='1'").fetchall()

    connection.close()

    return rows