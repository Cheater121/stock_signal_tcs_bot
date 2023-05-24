from datetime import datetime

def time_checker():
    now = datetime.now()
    if now.minute == 5:
        return True