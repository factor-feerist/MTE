import cmd
import os
import asyncio
from modules.gui import Gui
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
        #self.MTE = None
        MTEShell.prompt = f'{self._current_directory}>'
        self._ws = websockets.sync.client.connect("ws://localhost:8765")
        print("Connection opened")

    def do_login(self, name):
        self._ws.send(f'login {name}')
        message = self._ws.recv()
        print(f"Received: {message}")

    def do_open(self, file_name):
        self._ws.send(f'open {file_name}')
        message = self._ws.recv()
        if message == "OK":
            text = self._ws.recv()
            #нужно запустить Gui(text) (вставить message как содержимое)
            #уйти на бесконечный цикл обработки операций от Gui
            #self._gui = Gui(text)
            #process_editing()
        else:
            print(f"File '{file_name}' doesn't exist")

    def do_new(self, file_name):
        self._ws.send(f'new {file_name}')
        message = self._ws.recv()
        if message == "OK":
            pass
            #нужно запустить Gui("")  (пустой)
            #уйти на бесконечный цикл обработки операций от Gui
            #self._gui = Gui("")
            #process_editing()
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

    #def process_editing():
        #while True:
            #cmd = (await) Gui.get_next_cmd()
            # если пусто - continue
            #self._ws.send(cmd)
            #message = self._ws.recv()

            #print(f"Received: {message}")
            #if cmd == "log out":
                #break


if __name__ == '__main__':
    MTEShell().cmdloop()
