import os
import sys
import random
import traceback
from urls import * 
from spotify import Spotify
from robinhood import Portfolio, Stock
from keep import Keep
from argparser import ArgParser
from helpers import *

class Bot:
    """someone to do my bidding"""
    def __init__(self):
        try:
            self.parser = ArgParser()
            self.__run()
        except Exception:
            traceback.print_exc()

    def __checkin(self, options=None):
        """opens urls i frequently check"""
        urls = {
            "-m": MAIL_URLS,
            "-s": SCHOOL_URLS,
            "-S": SOCIAL_URLS
        }
        if options == None:
            return
        for option in options:
            open_urls(urls[option])

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
            f"{hl('checkin', 94)} [-m] [-s] [-S]\n"
            "\t-m: open email accounts\n"
            "\t-s: open school related tabs\n"
            "\t-S: open socials\n\n"
            f"{hl('note', 94)} [-n] [-k] [-o dir_path | -i dir_path]\n"
            "\t-n:          open notepad\n"
            "\t-k:          open gkeep\n"
            "\t-o dir_path: push notes from dir_path to gkeep\n"
            "\t-i dir_path: pull notes from gkeep to dir_path\n"
            "\tdir_path:    path to txt file directory to push/pull to/from\n\n"
            f"{hl('spotify', 94)} [-p [song] | -s [search_term]]\n"
            "\t-p:          play on open\n"
            "\t-s:          search on open\n"
            "\tsong:        name of song to play\n"
            "\tsearch_term: name of artist/song/album/playlist to search\n\n"
            f"{hl('stocks', 94)} [-v] [-o] [-s ticker]\n"
            "\t-v:        show portfolio value and daily profit/loss\n"
            "\t-o:        open robinhood\n"
            "\t-s ticker: get information about a particular stock\n"
            "\tticker:    ticker/stock symbol"
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
            "checkin": self.__checkin,
            "spotify": self.__spotify,
            "note": self.__note,
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