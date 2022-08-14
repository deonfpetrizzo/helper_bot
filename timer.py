import time
import msvcrt
import datetime
from threading import Thread
from playsound import playsound

class Timer:
    def __init__(self):
        pass

    def pomodoro(self, work_min, break_min):
        '''starts a pomodoro timer in a new thread'''
        def pom():
            self.cntdown(work_min, 'W -->')
            self.chime()
            self.cntdown(break_min, 'B -->')
            self.chime()
        self.start_thread(pom)

    def regular(self, mins):
        '''starts a countdown timer in a new thread'''
        def reg():
            self.cntdown(mins, '-->')
            self.chime()
        self.start_thread(reg)

    def start_thread(self, thread):
        '''starts a new thread'''
        active_thread = Thread(target=thread, daemon=True)
        active_thread.start()

    def chime(self):
        '''plays an alarm-like sound'''
        for i in range(3):
            playsound('resources/note.mp3')

    def cntdown(self, mins, txt):
        '''runs a count down timer and displays the time remaining'''
        sec = mins*60
        while sec >= 0:  
            timer = datetime.timedelta(seconds=sec)
            print(txt, timer, end='\n' if sec == 0 else '\r')
            time.sleep(1)
            sec -= 1
            