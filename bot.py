import os
import sys
import inspect
import traceback
from urls import * 
from spotify import Spotify
from robinhood import Portfolio
from robinhood import Stock
from keep import Keep
from argparser import ArgParser
from helpers import *

class Bot:
    """someone to do my bidding"""
    def __init__(self):
        try:
            self.parser = ArgParser()
            self.__run()
        except Exception as e:
            print(e)
            print(
                f"error:     invalid cmd\n"
                f"list cmds: py {sys.argv[0]} help"
            )

    def __mail(self):
        """opens my email accounts"""
        open_urls(MAIL_URLS)

    def __math(self):
        """opens math related tabs"""
        open_urls(CALC_URLS)

    def __school(self):
        """opens school related tabs"""
        open_urls(SCHOOL_URLS)

    def __social(self):
        """opens socials"""
        open_urls(SOCIAL_URLS)

    def __note(self, options=None, path=None):
        """opens note-taking apps or saves to/from gkeep"""
        self.keep = Keep("res/gkeep-login.json")
        if options == None:
            self.keep.open()
            os.startfile("notepad")
            return
        for option in options:
            if option == "-k":
                open_urls(KEEP_URL)
            elif option == "-n":
                os.startfile("notepad")
            elif option == "-o":
                self.keep.push(path)
            elif option == "-i":
                self.keep.pull(path)

    def __spotify(self, options=None, search_string=None):
        """opens spotify"""
        self.spotify = Spotify()
        self.spotify.open()
        if options[0] == "-p":
            self.spotify.play(search_string)
        elif options[0] == "-s":
            self.spotify.search(search_string)

    def __stocks(self, options=None, ticker=None):
        if options == None: 
            open_urls(ROBINHOOD_URL)
            return
        for option in options:
            if option == "-v":
                self.portfolio = Portfolio("res/robinhood-login.json")
                self.portfolio.value()
            elif option == "-o":
                open_urls(ROBINHOOD_URL)
            elif option == "-s":
                pass

    def __help(self):
        """displays all usages and their summaries"""
        help_msg = (
            f"py {self.parser.prog_name} <cmd>\n"
            "cmds:   mail\n"
            "\tschool\n"
            "\tmath\n"
            "\tsocial\n"
            "\thelp\n"
            "\tnote [-n] [-k] [-o dir_path | -i dir_path]\n"
            "\t\t-n:          open notepad\n"
            "\t\t-k:          open gkeep\n"
            "\t\t-o dir_path: push notes from dir_path to gkeep\n"
            "\t\t-i dir_path: pull notes from gkeep to dir_path\n"
            "\t\tdir_path:    path to txt file directory to push/pull to/from\n"
            "\tspotify [-p [song] | -s [search_term]]\n"
            "\t\t-p:          play on open\n"
            "\t\t-s:          search on open\n"
            "\t\tsong:        name of song to play\n"
            "\t\tsearch_term: name of artist/song/album/playlist to search\n"
            "\tstocks [-v] [-o] [-s ticker]\n"
            "\t\t-v:        show portfolio value and daily profit/loss\n"
            "\t\t-o:        open robinhood\n"
            "\t\t-s ticker: get information about a particular stock\n"
            "\t\tticker:    ticker/stock symbol\n"
        )
        print(help_msg)

    def __run(self):
        """parses string commands and assigns them to functions"""
        cmd = self.parser.cmd
        args = self.parser.args
        options = self.parser.opts
        nargs = len(args)
        nopts = len(options)
        cmds = {
            "mail": self.__mail,
            "math": self.__math,
            "school": self.__school,
            "spotify": self.__spotify,
            "note": self.__note,
            "social": self.__social,
            "stocks": self.__stocks,
            "help": self.__help
        }  
        if nopts != 0 and nargs != 0:
            cmds[cmd](options, *args[:nargs])
        elif nopts != 0 and nargs == 0:
            cmds[cmd](options)
        elif nopts == 0 and nargs != 0:
            cmds[cmd](*args[:nargs])
        else:
            cmds[cmd]()

if __name__ == "__main__":
    bot = Bot()