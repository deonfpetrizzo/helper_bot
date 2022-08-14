import os
import sys
import time 
import webbrowser 
import traceback
from timer import Timer
from notemanager import NoteManager
from constants import * 

class PersonalBot:
    def __init__(self):
        self.timer = Timer()
        self.note_manager = NoteManager('resources/gkeep-login.json')

    def run_cmd(self, cmd):
        '''parses string commands and arguments and runs the corresponding functions'''
        cmds = {'mail' : self.mail,
                'm' : self.mail,
                'calculator' : self.calculator,
                'c' : self.calculator,
                'school' : self.school,
                's' : self.school,
                'github' : self.github,
                'gh' : self.github,
                'monkeytype' : self.monkeytype,
                'mt' : self.monkeytype,
                'spotify' : self.spotify,
                'sp' : self.spotify,
                'notepad' : self.notepad,
                'np' : self.notepad,
                'notes.pull' : self.note_manager.pull, 
                'n.pull' : self.note_manager.pull,
                'notes.push' : self.note_manager.push,
                'n.push' : self.note_manager.push,
                'timer' : self.timer.regular,
                't' : self.timer.regular,
                'pomodoro' : self.timer.pomodoro,
                'p' : self.timer.pomodoro,
                'help' : self.help,
                'h' : self.help,
                'quit' : sys.exit,
                'q' : sys.exit,
                'exit' : sys.exit,
                'e' : sys.exit}
        try:
            tkns = cmd.split()
            if len(tkns) == 1:
                cmds[tkns[0].lower()]()
            elif len(tkns) == 2:
                cmds[tkns[0].lower()](float(tkns[1]))
            else:
                cmds[tkns[0].lower()](float(tkns[1]), float(tkns[2]))
        except TypeError:
            exception_data = traceback.format_exc().splitlines()
            print(exception_data[len(exception_data)-1])
        except KeyError:
            print('invalid command')
        except IndexError:
            pass
            
    def mail(self):
        '''opens all my email accounts'''
        self.open_urls(MAIL_URLS)

    def calculator(self):
        '''opens math related tabs'''
        self.open_urls(CALC_URLS)

    def school(self):
        '''opens school related tabs'''
        self.open_urls(SCHOOL_URLS)

    def github(self):
        '''opens my github profile'''
        self.open_urls(GITHUB_URL)

    def monkeytype(self):
        '''opens monkeytype'''
        self.open_urls(MONKEYTYPE_URL)

    def spotify(self):
        '''opens spotify'''
        os.startfile('spotify')

    def notepad(self):
        '''opens notepad'''
        os.startfile('notepad')

    def help(self):
        '''displays all available commands'''
        dat = [['.command.', '.shortcut.', '.function.'],
               ['mail', 'm', self.mail.__doc__],
               ['calculator', 'c', self.calculator.__doc__],
               ['school', 's', self.school.__doc__],
               ['github', 'gh', self.github.__doc__],
               ['monkeytype', 'mt', self.monkeytype.__doc__],
               ['spotify', 'sp', self.spotify.__doc__],
               ['notepad', 'np', self.notepad.__doc__],
               ['notes.push', 'n.push', self.note_manager.push.__doc__],
               ['notes.pull', 'n.pull', self.note_manager.pull.__doc__],
               ['timer', 't', self.timer.regular.__doc__],
               ['pomodoro', 'p', self.timer.pomodoro.__doc__],
               ['quit', 'q', 'exit'],
               ['exit', 'e', 'exit']]
        for d in dat:
            row = ''
            for e in d:
                row += e.ljust(MAX_CMD_LEN+4)
            print(row)

    def open_urls(self, urls):
        '''opens an arbitrary number of tabs'''
        for url in urls:
            webbrowser.open_new(url)
            time.sleep(1)

if __name__ == '__main__':
    bot = PersonalBot()
    while True:
        bot.run_cmd(input())
