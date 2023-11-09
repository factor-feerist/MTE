import cmd
import os
from modules.gui import Gui
from modules.edit_manager import EditManager
import websockets.sync.client
try:
    import websockets.sync.client
except ImportError:
    import pip
    package = "websockets.sync.client"
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
    import websockets.sync.client


class MTEShell(cmd.Cmd):
    intro = 'Welcome to the MTE shell'
    prompt = None

    def __init__(self):
        super().__init__()
        self._current_directory = os.getcwd()
        MTEShell.prompt = f'{self._current_directory}>'
        self._ws = websockets.sync.client.connect("ws://localhost:8765")
        self.username = ''
        self.file_name = ''
        print("Connection opened")

    def do_login(self, name):
        self._ws.send(f'login {name}')
        message = self._ws.recv()
        print(f"Received: {message}")
        self.username = name

    def do_open(self, file_name):
        self._ws.send(f'open {file_name}')
        message = self._ws.recv()
        if message == "OK":
            self.file_name = file_name
            text = self._ws.recv()
            operations_handler = EditManager(text, self._ws, self.file_name, self.username)
            gui = Gui(operations_handler, text, self.file_name, self.username)
            gui.run()
            # нужно запустить Gui(text) (вставить message как содержимое)
            # уйти на бесконечный цикл обработки операций от Gui
            # self._gui = Gui(text)
            # process_editing()
        else:
            print(f"File '{file_name}' doesn't exist")

    def do_new(self, file_name):
        self._ws.send(f'new {file_name}')
        message = self._ws.recv()
        if message == "OK":
            self.file_name = file_name
            operations_handler = EditManager('', self._ws, self.file_name, self.username)
            gui = Gui(operations_handler, '', self.file_name, self.username)
            gui.run()
            # нужно запустить Gui("")  (пустой)
            # уйти на бесконечный цикл обработки операций от Gui
            # self._gui = Gui("")
            # process_editing()
        else:
            print(f"File '{file_name}' already exists")

    """def do_cd(self, directory):
        'Changes current directory\n> cd directory'
        try:
            if ':' in directory:
                os.chdir(directory)
                self._current_directory = directory
            else:
                os.chdir(os.path.join(self._current_directory, directory))
                self._current_directory = os.path.join(self._current_directory,
                                                       directory)
            MTEShell.prompt = f'{self._current_directory}>'
        except OSError:
            print(f'*** Can\'t find directory \"{directory}\"')
    """

    """def do_mkdir(self, directory):
        'Creates a new directory\n> mkdir directory'
        try:
            os.mkdir(os.path.join(self._current_directory, directory))
        except FileExistsError:
            print(f'*** Directory {directory} already exists')
    """

    """def do_touch(self, filename):
        'Creates a new file\n> touch file'
        try:
            with open(filename):
                print(f'*** File {filename} already exists')
        except OSError:
            with open(filename, 'w'):
                pass
    """

    """def do_ls(self, arg):
        'Shows all files in current directory\n> ls'
        for item in os.listdir(self._current_directory):
            print(f'    {item}')
    """

    def precmd(self, line):
        print()
        return line


if __name__ == '__main__':
    MTEShell().cmdloop()
