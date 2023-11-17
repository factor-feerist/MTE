import sys
import os
import cmd
import threading
import time
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

    def runtk(self, text, edit=True):
        self.operations_handler = EditManager(text, self._ws,
                                              self.filename, self.username)
        self.gui = Gui(self.operations_handler, text,
                       self.filename, self.username, edit)
        self.gui.window.mainloop()

    def do_login(self, name):
        'Log user in\n> login username'
        if len(name) == 0:
            print("Incorrect name!")
            return
        self._ws.send(f'l {name}')
        message = self._ws.recv()
        print(f"Received: {message}")
        self.username = name

    def do_logout(self, _line):
        'Log user out\n> logout'
        self._ws.send('lo')
        message = self._ws.recv()
        print(message)
        time.sleep(2)
        sys.exit(0)

    def do_open(self, filename):
        'Open existing file to edit online\n> open filename'
        self._ws.send(f'o {filename}')
        message = self._ws.recv()
        if message == "OK":
            self.filename = filename
            text = self._ws.recv()
            gui_thread = threading.Thread(target=self.runtk, args=(text, ))
            gui_thread.daemon = True
            gui_thread.start()
            time.sleep(0.1)
            while True:
                time.sleep(0.01)
                if self.gui.save_is_pressed:
                    self.save()
                    self.gui.save_is_pressed = False
                if self.gui.is_closed:
                    self.close()
                    gui_thread.join(0.05)
                    break
                try:
                    text = self._ws.recv(timeout=0.01)
                    self.gui.update_text(text, self.operations_handler)
                except TimeoutError:
                    command = self.operations_handler.get_next_command()
                    if len(command) != 0:
                        self._ws.send(command)
        else:
            print(message)

    def do_new(self, filename):
        'Creates new file to edit online\n> new filename'
        self._ws.send(f'n {filename}')
        message = self._ws.recv()
        if message == "OK":
            self.filename = filename
            gui_thread = threading.Thread(target=self.runtk, args=('', ))
            gui_thread.daemon = True
            gui_thread.start()
            time.sleep(0.1)
            while True:
                time.sleep(0.01)
                if self.gui.save_is_pressed:
                    self.save()
                    self.gui.save_is_pressed = False
                if self.gui.is_closed:
                    self.close()
                    gui_thread.join(0.05)
                    break
                try:
                    text = self._ws.recv(timeout=0.01)
                    self.gui.update_text(text, self.operations_handler)
                except TimeoutError:
                    command = self.operations_handler.get_next_command()
                    if len(command) != 0:
                        self._ws.send(command)
        else:
            print(message)

    def do_watch(self, line):
        'Shows existing file, changes won\'t appear or save\n' \
            '> watch filename version\n' \
            '> watch filename = watch filename "actual"'
        ops = line.split()
        version = "actual"
        if len(ops) >= 2:
            version = ops[1]
        self._ws.send(f'w {ops[0]} {version}')
        message = self._ws.recv()
        if message == "OK":
            self.filename = ops[0]
            text = self._ws.recv()
            gui_thread = threading.Thread(target=self.runtk,
                                          args=(text, False,))
            gui_thread.daemon = True
            gui_thread.start()
            time.sleep(0.1)
            while True:
                time.sleep(0.01)
                if self.gui.is_closed:
                    self.close()
                    gui_thread.join(0.05)
                    break
        else:
            print(message)

    def do_log(self, filename):
        'Shows file changes log\n> log filename'
        self._ws.send(f'wl{filename}')
        message = self._ws.recv()
        if message == "OK":
            self.filename = filename
            text = self._ws.recv()
            gui_thread = threading.Thread(target=self.runtk,
                                          args=(text, False,))
            gui_thread.daemon = True
            gui_thread.start()
            time.sleep(0.1)
            while True:
                time.sleep(0.01)
                if self.gui.is_closed:
                    self.close()
                    gui_thread.join(0.05)
                    break
        else:
            print(message)

    def save(self):
        self._ws.send(f's {self.filename} {self.username}')
        message = self._ws.recv()
        if message == "OK":
            message = self._ws.recv()
        print(message)

    def close(self):
        self._ws.send(f'c {self.username}')
        message = self._ws.recv()
        if message == "OK":
            message = self._ws.recv()
        print(message)

    def precmd(self, line):
        print()
        return line


if __name__ == '__main__':
    MTEShell().cmdloop()
