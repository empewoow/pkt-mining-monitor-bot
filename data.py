import sqlite3

database_name = "data.db"

def create_table():

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE addresses (chat_id INTEGER, address TEXT)")

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
            return "No addresses yet!"
        else:
            addresses = ""
            for row in rows:
                addresses += str(row[0]) + "\n"
            return "Addresses:\n" + addresses

def add_address(chat_id, message):

    strings = message.split()

    if len(strings) != 2:
        return "Syntax error. Use /help for more info."
    else:
        strings.remove("/add_address")
        address = strings[0]

        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO addresses VALUES ('" + str(chat_id) + "', '" + address + "')")

        connection.commit()
        connection.close()

        return "PKT address " + address + " added!"

def remove_address(chat_id, message):

    strings = message.split()

    if len(strings) != 2:
        return "Syntax error. Use /help for more info."
    else:
        strings.remove("/remove_address")
        address = strings[0]

        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM addresses WHERE chat_id='" + str(chat_id) + "' AND address='" + address + "'")

        connection.commit()
        connection.close()

        return "PKT address " + address + " removed..."

def get_first_address(chat_id):

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    
    rows = cursor.execute("SELECT address FROM addresses WHERE chat_id='" + str(chat_id) + "'").fetchall()

    connection.close()

    return rows[0][0]

def get_all_addresses(chat_id):

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
