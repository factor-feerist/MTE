import cmd
import os
import threading
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
        self.filename = ''
        self.operations_handler = None
        self.gui = None
        print("Connection opened")


    def runtk(self, text):
        self.operations_handler = EditManager(text, self._ws, self.filename, self.username)
        self.gui = Gui(self.operations_handler, text, self.filename, self.username)                         
        self.gui.window.mainloop()


    def do_login(self, name):
        if len(name) == 0:
            print("Incorrect name!")
            return
        self._ws.send(f'l {name}')
        message = self._ws.recv()
        print(f"Received: {message}")
        self.username = name


    def do_logout(self):
        self._ws.send('lo')
        # закрыть консоль


    def do_open(self, filename):
        self._ws.send(f'o {filename}')
        message = self._ws.recv()
        if message == "OK":
            self.filename = filename
            text = self._ws.recv()
            gui_thread = threading.Thread(target=self.runtk, args = (text, ))
            gui_thread.daemon = True
            gui_thread.start()
            # нужно запустить Gui(text) (вставить message как содержимое)
            # уйти на бесконечный цикл обработки операций от Gui
            # self._gui = Gui(text)
            # process_editing()
            while True:
                try:
                    text = self._ws.recv(timeout=0.01)
                    self.gui.update_text(text, self.operations_handler)
                except TimeoutError:
                    cmd = self.operations_handler.get_next_command()
                    if len(cmd) != 0:
                        self._ws.send(cmd)
        else:
            print(message)


    def do_new(self, filename):
        self._ws.send(f'n {filename}')
        message = self._ws.recv()
        if message == "OK":
            self.filename = filename
            #operations_handler = EditManager('', self._ws, self.filename, self.username)
            #gui = Gui(operations_handler, '', self.filename, self.username)
            #теперь это делает функция
            gui_thread = threading.Thread(target=self.runtk, args = ('', ))
            gui_thread.daemon = True
            gui_thread.start()
            while True:
                try:
                    text = self._ws.recv(timeout=0.01)
                    self.gui.update_text(text, self.operations_handler)
                except TimeoutError:
                    cmd = self.operations_handler.get_next_command()
                    if len(cmd) != 0:
                        self._ws.send(cmd)
        else:
            print(message)

    
    def do_save(self, filename):
        self._ws.send(f's {filename}')
        message = self._ws.recv()
        if message == "OK":
            message = self._ws.recv()
        print(message)


    def do_watch(self, filename):
        self._ws.send(f'w {filename}')
        text = self._ws.recv()
        # открыть файл без возможности редактирования


    def precmd(self, line):
        print()
        return line


if __name__ == '__main__':
    MTEShell().cmdloop()
