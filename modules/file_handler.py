import os
from datetime import datetime


class FileHandler:
    def __init__(self):
        self._current_directory = os.getcwd()
        os.mkdir(f'{self._current_directory}\\.rep')
        os.mkdir(f'{self._current_directory}\\.rep\\files')
        with open(f'{self.directory}\\.rep\\log', 'w'):
            pass
        with open(f'{self.directory}\\.rep\\users', 'w'):
            pass
    

    def new(self, filename, username):
        if os.path.isdir(f'{self._current_directory}\\.rep\\files\\filename'):
            raise Exception(f'File {filename} already exists')
        os.mkdir(f'{self._current_directory}\\.rep\\files\\filename')
        with open(f'{self.directory}\\.rep\\files\\filename\\actual', 'w'):
            pass
        with open(f'{self.directory}\\.rep\\files\\filename\\actual_version', 'w'):
            f.write('0')
        with open(f'{self.directory}\\.rep\\users', 'a') as f:
            f.write(f'{filename}\\\\{username}')
        with open(f'{self.directory}\\.rep\\log', 'a') as f:
            f.write(f'{filename} created by {username} at {datetime.now().strftime("%d/%m/%y %H:%M:%S")}')


    def open(self, filename, username):
        if not os.path.isdir(f'{self._current_directory}\\.rep\\files\\filename'):
            raise Exception(f'File {filename} doesn\'t exist')
        with open(f'{self.directory}\\.rep\\users', 'a') as f:
            f.write(f'{filename}\\\\{username}')
        with open(f'{self._current_directory}\\.rep\\files\\filename\\actual'):
            return f.read()


    def save(self, filename):
        if not os.path.isdir(f'{self._current_directory}\\.rep\\files\\filename'):
            raise Exception(f'File {filename} doesn\'t exist')
        with open(f'{self.directory}\\.rep\\files\\filename\\actual'):
            text = f.read()
        with open(f'{self.directory}\\.rep\\files\\filename\\actual_version', 'w'):
            version = int(f.read())
            f.write(version + 1)
        with open(f'{self.directory}\\.rep\\files\\filename\\{version}', 'w'):
            f.write(text)
        with open(f'{self.directory}\\.rep\\log', 'a') as f:
            f.write(f'{filename} v.{version} saved by {username} at {datetime.now().strftime("%d/%m/%y %H:%M:%S")}')


    def watch(self, filename, version):
        if not os.path.isdir(f'{self._current_directory}\\.rep\\files\\filename'):
            raise Exception(f'File {filename} doesn\'t exist')
        if not os.path.exists(f'{self._current_directory}\\.rep\\files\\filename\\{version}'):
            raise Exception(f'File {filename} v.{version} doesn\'t exist')
        with open(f'{self._current_directory}\\.rep\\files\\filename\\{version}') as f:
            return f.read()

    def add(self, filename, username, to_add, index):
        with open(f'{self._current_directory}\\.rep\\files\\filename\\actual', 'w') as f:
            text = f.read()
            f.write(text[:index] + to_add + text[index:])
        with open(f'{self.directory}\\.rep\\log', 'a') as f:
            f.write(f'{filename}:\n    {to_add}\nwas added by {username} at {datetime.now().strftime("%d/%m/%y %H:%M:%S")}')

    def remove(self, filename, username, to_remove, index):
        count = len(to_remove)
        with open(f'{self._current_directory}\\.rep\\files\\filename\\actual', 'w') as f:
            text = f.read()
            f.write(text[:index] + text[index + count:])
        with open(f'{self.directory}\\.rep\\log', 'a') as f:
            f.write(f'{filename}:\n    {to_remove}\nwas removed by {username} at {datetime.now().strftime("%d/%m/%y %H:%M:%S")}')
