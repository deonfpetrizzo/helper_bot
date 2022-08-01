import time
import datetime
import threading 
from helpers import pad
from playsound import playsound

class Pomodoro:
    def __init__(self):
        pass

    def start_timer_thread(self, work_mins, break_mins):
        """starts a pomodoro timer in a new thread"""
        def pomodoro():
            work_seconds = work_mins * 60
            break_seconds = break_mins * 60

            self.count_down(work_seconds, "---> work:")
            self.chime()

            self.count_down(break_seconds, "---> break:")
            self.chime()

        p_thread = threading.Thread(target=pomodoro, daemon=True)
        p_thread.start()

    def chime(self):
        """plays an alarm-like sound"""
        for i in range(3):
            playsound("note.mp3")

    def count_down(self, sec, txt):
        """runs a count down timer and displays the time remaining"""
        while sec >= 0:
            timer = datetime.timedelta(seconds=sec)
            print(txt, timer, end="\n" if sec == 0 else "\r")
            time.sleep(1)
            sec -= 1
            