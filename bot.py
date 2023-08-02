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
            self.__help()

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
        """opens note-taking apps, saves to/from gkeep"""
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
        """opens robinhood, displays portfolio/ticker performance"""
        if options == None: 
            open_urls(ROBINHOOD_URL)
            return
        for option in options:
            if option == "-v":
                self.portfolio = Portfolio("res/robinhood-login.json")
                self.portfolio.performance()
            elif option == "-o":
                open_urls(ROBINHOOD_URL)
            elif option == "-s":
                pass

    def __help(self, base_cmd="help"):
        """prints usage statements"""
        checkin_usg = (
            f"{hl('c, checkin', 94)} [{hl('-h', 93)}] | [-m -s -S]\n"
            "\t-m: open email accounts\n"
            "\t-s: open school related tabs\n"
            "\t-S: open socials"
        )
        note_usg = (
            f"{hl('n, note', 94)} [{hl('-h', 93)}] | [-n -k] [-o dir_path | -i dir_path]\n"
            "\t-n:          open notepad\n"
            "\t-k:          open gkeep\n"
            "\t-o dir_path: push notes from dir_path to gkeep\n"
            "\t-i dir_path: pull notes from gkeep to dir_path\n"
            "\tdir_path:    path to txt file directory to push/pull to/from"
        )
        spotify_usg = (
            f"{hl('s, spotify', 94)} [{hl('-h', 93)}] | [-p [song] | -s [search_term]]\n"
            "\t-p:          play on open\n"
            "\t-s:          search on open\n"
            "\tsong:        name of song to play\n"
            "\tsearch_term: name of artist/song/album/playlist to search"
        )
        stocks_usg = (
            f"{hl('$, stocks', 94)} [{hl('-h', 93)}] | [-v -o -s ticker]\n"
            "\t-v:        show portfolio value and daily profit/loss\n"
            "\t-o:        open robinhood\n"
            "\t-s ticker: get information about a particular stock\n"
            "\tticker:    ticker/stock symbol"
        )
        help_usg = f"{hl('h, help', 94)}"
        help_msg = (
            f"{checkin_usg}\n"
            f"{note_usg}\n"
            f"{spotify_usg}\n"
            f"{stocks_usg}\n"
            f"{help_usg}\n"
            f"{hl('-h', 93)}: print specific usage statement"
        )
        output_msg = {
            "checkin": checkin_usg,
            "c": checkin_usg,
            "spotify": spotify_usg,
            "s": spotify_usg,
            "note": note_usg,
            "n": note_usg,
            "stocks": stocks_usg,
            "$": stocks_usg,
            "help": help_msg,
            "h": help_msg
        }
        print(output_msg[base_cmd], end="\n\n")

    def __run(self):
        """parses string commands and assigns them to functions"""
        cmd = self.parser.cmd
        args = self.parser.args
        options = self.parser.opts
        nargs = len(args)
        nopts = len(options)
        cmds = {
            "checkin": self.__checkin,
            "c": self.__checkin,
            "spotify": self.__spotify,
            "s": self.__spotify,
            "note": self.__note,
            "n": self.__note,
            "stocks": self.__stocks,
            "$": self.__stocks,
            "help": self.__help,
            "h": self.__help
        }  
        for opt in options:
            if opt == "-h":
                self.__help(cmd)
                return
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