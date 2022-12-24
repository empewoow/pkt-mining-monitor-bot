import sqlite3

# https://github.com/J4NN0/j4nn0-b0t/blob/master/util/reminder.py

database_name = "data.db"

def create_table():

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS addresses (chat_id INTEGER, address TEXT)")

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
        strings.remove("/add_address")
        address = strings[0]

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
        strings.remove("/remove_address")
        address = strings[0]

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

#create_table()

#add_address("89012380", "/add_address pktaddress3")
#list_addresses()

#add_address("/add_address pktaddress1 asdasd")

#remove_address("89012380", "/remove_address pktaddress3")
#list_addresses()

#remove_address("/remove_address pktaddress1 asdasd")
