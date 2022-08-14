import os
import sys
import time 
import webbrowser 
from pomodoro import Pomodoro
from notemanager import NoteManager
from constants import * 

class PersonalBot:
    def __init__(self):
        self.pom = Pomodoro()
        self.n_mgr = NoteManager('resources/gkeep-login.json')

    def run_cmd(self, cmd):
        '''parses string commands and arguments and runs the corresponding functions'''
        cmds = {
            'mail' : self.mail,
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
            'notes.pull' : self.n_mgr.pull, 
            'n.pull' : self.n_mgr.pull,
            'notes.push' : self.n_mgr.push,
            'n.push' : self.n_mgr.push,
            'pomodoro' : self.pom.start_timer_thread,
            'p' : self.pom.start_timer_thread,
            'help' : self.help,
            'h' : self.help,
            'quit' : sys.exit,
            'q' : sys.exit,
            'exit' : sys.exit,
            'e' : sys.exit
        }
    
        try:
            tkns = cmd.split()
            if len(tkns) > 1:
                cmds[tkns[0].lower()](float(tkns[1]), float(tkns[2]))
            else:
                cmds[tkns[0].lower()]()
        except KeyError:
            print('invalid cmd')
        except TypeError:
            print('enter args')
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
        dat = [['.command.', '.shortcut.', '.function.', '.arguments.'],
               ['mail', 'm', self.mail.__doc__],
               ['calculator', 'c', self.calculator.__doc__],
               ['school', 's', self.school.__doc__],
               ['github', 'gh', self.github.__doc__],
               ['monkeytype', 'mt', self.monkeytype.__doc__],
               ['spotify', 'sp', self.spotify.__doc__],
               ['notepad', 'np', self.notepad.__doc__],
               ['notes.push', 'n.push', self.n_mgr.push.__doc__],
               ['notes.pull', 'n.pull', self.n_mgr.pull.__doc__],
               ['pomodoro', 'p', self.pom.start_timer_thread.__doc__, 'work_minutes break_minutes'],
               ['quit', 'q', 'exit'],
               ['exit', 'e', 'exit']]

        for d in dat:
            row = ''
            cnt = 0
            for e in d:
                str_len = MAX_CMD_LEN+4 if cnt < 2 else MAX_COMMENT_LEN+4
                row += e.ljust(str_len)
                cnt += 1
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
