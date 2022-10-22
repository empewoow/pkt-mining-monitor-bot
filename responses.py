from datetime import datetime

def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello", "sup"):
        return "Hey, how are you?"

    if user_message in ("time"):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M")
        return str(date_time)

    if user_message in ("best coin"):
        return "Bitcoin of course!"
    
    return "I don't understand..."