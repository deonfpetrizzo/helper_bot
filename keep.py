import os
import json
import gkeepapi
from helpers import *

class Keep:
    """link between notepad and gkeep"""
    def __init__(self, acct_file_path):
        self.acct_file_path = acct_file_path

    def __login(self):
        """logs into gkeepapi"""
        with open(self.acct_file_path, "r", encoding="utf-8") as f:
            acct = json.load(f)
        self.keep = gkeepapi.Keep()
        self.keep.login(acct["username"], acct["password"])

    def __get_txt_paths(self, dir_path):
        """returns a list of all txt file paths in the notes directory"""
        paths = []
        for filename in os.listdir(dir_path):
            path = os.path.join(dir_path, filename)
            if os.path.isfile(path) and path[path.rfind("."):] == ".txt":
                paths.append(path)
        return paths

    def __get_keep_notes(self):
        """retrieves all notes in my gkeep acct"""
        self.__login()
        return self.keep.all()

    def open(self):
        """opens gkeep in a new tab"""
        open_urls(KEEP_URL)

    def push(self, dir_path):
        """transfers txt file data to gkeep"""
        notes = self.__get_keep_notes()
        paths = self.__get_txt_paths(dir_path)
        does_note_exist = False
        for path in paths:
            title = path[path.rfind("\\")+1 : path.rfind(".")]
            body = ""
            with open (path, mode="r", encoding="utf-8") as f:
                body = f.read()
            for note in notes:
                if note.title == title:
                    note.text = body
                    does_note_exist = True
                    break
                does_note_exist = False
            if not does_note_exist:
                self.keep.createNote(title, body)
        self.keep.sync()

    def pull(self, dir_path):
        """updates txt files to match corresponding gkeep notes"""
        notes = self.__get_keep_notes()
        paths = self.__get_txt_paths(dir_path)
        for path in paths:
            title = path[path.rfind("\\")+1 : path.rfind(".")]
            for note in notes:
                if note.title == title:
                    with open (path, mode="w", encoding="utf-8") as f:
                        f.write(note.text)
                    break
