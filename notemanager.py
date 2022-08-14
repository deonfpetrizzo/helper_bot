import os
import json
import gkeepapi

class NoteManager:
    def __init__(self, acct_file_path):
        self.acct_file_path = acct_file_path

    def login(self):
        '''logs into gkeepapi using user credentials'''
        with open(self.acct_file_path, 'r', encoding='utf-8') as f:
            acct = json.load(f)
        self.keep = gkeepapi.Keep()
        self.keep.login(acct['username'], acct['password'])

    def get_txt_file_paths(self):
        '''returns a list of all txt file paths in the notes directory'''
        directory = 'notes'
        paths = []
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            if os.path.isfile(path):
                paths.append(path)
        return paths

    def push(self):
        '''transfers txt file data to gkeep'''
        self.login()
        paths = self.get_txt_file_paths()
        notes = self.keep.all() 
        does_note_exist = False
        for path in paths:
            title = path[path.index('\\')+1 : path.index('.')]
            body = ''
            with open (path, 'r') as f:
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

    def pull(self):
        '''updates txt files to match corresponding gkeep notes'''
        self.login()
        paths = self.get_txt_file_paths()
        notes = self.keep.all()
        for path in paths:
            title = path[path.index('\\')+1 : path.index('.')]
            for note in notes:
                if note.title == title:
                    with open (path, 'w') as f:
                        f.write(note.text)
                    break