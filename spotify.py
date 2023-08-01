import os
import time
import pyautogui as pag

class Spotify:
    """simple spotify automation"""
    def __init__(self):
        pass

    def open(self):
        """opens spotify and waits"""
        os.startfile("spotify")
        time.sleep(5)

    def play(self, song=None):
        """searches and plays song or plays current que if song=None"""
        if song != None:
            self.search(song)
            for key in ["enter", "tab", "enter", "enter"]:
                time.sleep(1)
                pag.press(key)
        else:
            pag.press("space")

    def search(self, search_terms=None):
        """enters search_terms into the spotify search bar"""
        pag.hotkey("ctrl", "l")
        if search_terms != None:
            time.sleep(0.5)
            pag.typewrite(search_terms, interval=0.02)