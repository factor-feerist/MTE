import os
from datetime import datetime


class FileHandler:
    def __init__(self):
        self._current_directory = os.getcwd()
        if not os.path.isdir(f'{self._current_directory}\\.rep'):
            os.mkdir(f'{self._current_directory}\\.rep')
        if not os.path.isdir(f'{self._current_directory}\\.rep\\files'):
            os.mkdir(f'{self._current_directory}\\.rep\\files')
        with open(f'{self._current_directory}\\.rep\\log', 'w'):
            pass
        with open(f'{self._current_directory}\\.rep\\users', 'w'):
            pass
    

    def new(self, filename, username):
        if os.path.isdir(f'{self._current_directory}\\.rep\\files\\{filename}'):
            raise Exception(f'File {filename} already exists')
        os.mkdir(f'{self._current_directory}\\.rep\\files\\{filename}')
        with open(f'{self._current_directory}\\.rep\\files\\{filename}\\actual', 'w'):
            pass
        with open(f'{self._current_directory}\\.rep\\files\\{filename}\\actual_version', 'w') as f:
            f.write('0')
        with open(f'{self._current_directory}\\.rep\\users', 'a') as f:
            f.write(f'{filename}\\\\{username}\n')
        with open(f'{self._current_directory}\\.rep\\log', 'a') as f:
            f.write(f'{filename} created by {username} at {datetime.now().strftime("%d/%m/%y %H:%M:%S")}\n')


    def open(self, filename, username):
        if not os.path.isdir(f'{self._current_directory}\\.rep\\files\\{filename}'):
            raise Exception(f'File {filename} doesn\'t exist')
        with open(f'{self._current_directory}\\.rep\\users', 'a') as f:
            f.write(f'{filename}\\\\{username}\n')
        with open(f'{self._current_directory}\\.rep\\files\\{filename}\\actual') as f:
            return f.read()


    def save(self, filename):
        if not os.path.isdir(f'{self._current_directory}\\.rep\\files\\{filename}'):
            raise Exception(f'File {filename} doesn\'t exist')
        with open(f'{self._current_directory}\\.rep\\files\\{filename}\\actual') as f:
            text = f.read()
        with open(f'{self._current_directory}\\.rep\\files\\{filename}\\actual_version', 'w') as f:
            version = int(f.read())
            f.write(version + 1)
        with open(f'{self._current_directory}\\.rep\\files\\{filename}\\{version}', 'w') as f:
            f.write(text)
        with open(f'{self._current_directory}\\.rep\\log', 'a') as f:
            f.write(f'{filename} v.{version} saved by {username} at {datetime.now().strftime("%d/%m/%y %H:%M:%S")}\n')


    def watch(self, filename, version):
        if not os.path.isdir(f'{self._current_directory}\\.rep\\files\\{filename}'):
            raise Exception(f'File {filename} doesn\'t exist')
        if not os.path.exists(f'{self._current_directory}\\.rep\\files\\{filename}\\{version}'):
            raise Exception(f'File {filename} v.{version} doesn\'t exist')
        with open(f'{self._current_directory}\\.rep\\files\\{filename}\\{version}') as f:
            return f.read()


    def add(self, filename, username, to_add, index):
        with open(f'{self._current_directory}\\.rep\\files\\{filename}\\actual', 'w') as f:
            text = f.read()
            text = text[:index] + to_add + text[index:]
            f.write(text)
        with open(f'{self._current_directory}\\.rep\\log', 'a') as f:
            f.write(f'{filename}:\n    {to_add}\nwas added by {username} at {datetime.now().strftime("%d/%m/%y %H:%M:%S")}\n')
        return text


    def remove(self, filename, username, to_remove, index):
        count = len(to_remove)
        with open(f'{self._current_directory}\\.rep\\files\\{filename}\\actual', 'w') as f:
            text = f.read()
            text = text[:index] + text[index + count:]
            f.write(text)
        with open(f'{self._current_directory}\\.rep\\log', 'a') as f:
            f.write(f'{filename}:\n    {to_remove}\nwas removed by {username} at {datetime.now().strftime("%d/%m/%y %H:%M:%S")}\n')
        return text

    def get_users_by_filename(self, filename):
        with open(f'{self._current_directory}\\.rep\\users') as f:
            users = f.read()
        result = []
        for line in users.split('\n'):
            ops = line.split('\\\\')
            if len(ops) == 2 and ops[0] == filename:
                result.append(ops[1])
        return result
