import sys 
import time 
import webbrowser 
from pomodoro import Pomodoro
from helpers import pad
from constants import MAIL_URLS, CALC_URLS, SCHOOL_URLS

class HelperBot:
    def __init__(self):
        print("cmd" + pad("", 7) + "out")
        self.pom = Pomodoro()

    def run_cmd(self, cmd):
        """parses string commands and arguments and runs the corresponding functions"""
        cmds = {
            "m" : self.mail,
            "c" : self.calc,
            "s" : self.school,
            "p" : self.pom.start_timer_thread,
            "h" : self.help,
            "q" : sys.exit,
            "e" : sys.exit
        }
        
        try:
            tkns = cmd.split()
            if len(tkns) > 1:
                cmds[tkns[0].lower()](float(tkns[1]), float(tkns[2]))
            else:
                cmds[tkns[0].lower()]()
        except KeyError:
            print(pad("invalid cmd", 10))
        except TypeError:
            print(pad("enter args", 10))
        except IndexError:
            pass

    def mail(self):
        """opens all my email accounts"""
        self.open_urls(MAIL_URLS)

    def calc(self):
        """opens math related tabs"""
        self.open_urls(CALC_URLS)

    def school(self):
        """opens school related tabs"""
        self.open_urls(SCHOOL_URLS)

    def help(self):
        """displays all available commands"""
        txts = ["m: " + self.mail.__doc__,
                "c: " + self.calc.__doc__,
                "s: " + self.school.__doc__,
                "p: " + self.pom.start_timer_thread.__doc__,
                "h: help",
                "q: exit",
                "e: exit"]

        for txt in txts:
            print(pad(txt, 10))

    def open_urls(self, urls):
        """opens an arbitrary number of tabs"""
        for url in urls:
            webbrowser.open_new(url)
            time.sleep(0.5)

if __name__ == "__main__":
    bot = HelperBot()
    while True:
        bot.run_cmd(input())
