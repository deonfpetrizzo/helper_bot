import os
import json
import gkeepapi

class NoteManager:
    def __init__(self, acct_file_path):
        with open(acct_file_path, 'r', encoding='utf-8') as f:
            acct = json.load(f)

        self.keep = gkeepapi.Keep()
        self.keep.login(acct['username'], acct['password'])

    def get_txt_file_paths(self):
        '''returns a list of all txt file paths in the notes directory'''
        directory = 'notes'
        txt_file_paths = []

        for file_name in os.listdir(directory):
            path = os.path.join(directory, file_name)

            if os.path.isfile(path):
                txt_file_paths.append(str(path))
        
        return txt_file_paths

    def push(self):
        '''transfers local txt file data to google keep'''
        txt_file_paths = self.get_txt_file_paths()
        notes = self.keep.all() 
        does_note_exist = False

        for txt_file_path in txt_file_paths:
            title = str(txt_file_path)[txt_file_path.index('\\')+1 : txt_file_path.index('.')]
            body = ''

            with open (txt_file_path, 'r') as f:
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
        '''updates the bodies of local txt files to match 
                            those of corresponding google keep notes'''
        txt_file_paths = self.get_txt_file_paths()
        gnotes = self.keep.all()

        for txt_file_path in txt_file_paths:
            title = str(txt_file_path)[txt_file_path.index('\\')+1 : txt_file_path.index('.')]

            for note in notes:
                if note.title == title:
                    with open (txt_file_path, 'w') as f:
                        f.write(note.text)
                    break


