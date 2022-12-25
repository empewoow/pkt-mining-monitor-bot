from datetime import datetime

def sample_responses(message):
    message = message.lower()

    if message in ("hello", "sup"):
        return "Hey, how are you?"

    if message in ("time"):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M")
        return str(date_time)

    if message in ("best coin"):
        return "Bitcoin of course!"
    
    return "I don't understand..."