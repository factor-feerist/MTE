#здесь интерфейс самого текстового редактора

import tkinter
import tkinter.ttk
from tkinter import Scrollbar, VERTICAL
from modules import text_editor


class Gui:
    def __init__(self, ws, text = ''):
        self.window = tkinter.Tk()
        self.text = tkinter.Text(self.window, width=400, height=400, wrap="word")
        self.text.insert('1.0', text)
        self.scrollbar = Scrollbar(self.window, orient=VERTICAL, command=self.text.yview)
        self.editor = text_editor.Editor()
        self.server = ws
        self.operations = text_editor.Operations(self.text, self.editor, self.server)
        self.menu = tkinter.Menu(self.window)
        self.file_menu = tkinter.Menu(self.menu, tearoff=0)
        self.setup_window()
        self.setup_scrollbar()
        self.setup_text()
        self.setup_file_menu()
        self.setup_menu()
        self.setup_key_bindings()

    def setup_window(self):
        self.window.minsize(width=500, height=500)
        self.window.maxsize(width=500, height=500)
        self.window.title("Text editor")
        self.window.config(menu=self.menu)

    def setup_text(self):
        self.text.configure(yscrollcommand=self.scrollbar.set)
        self.text.pack()

    def setup_scrollbar(self):
        self.scrollbar.pack(side="right", fill="y")

    def setup_file_menu(self):
        self.file_menu.add_command(label="Save file", command=self.operations.save_file)

    def setup_key_bindings(self):
        self.window.bind("<Key>", self.operations.process_keyboard_event)

    def setup_menu(self):
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="Info", command=self.operations.show_info)

    def run(self):
        self.window.mainloop()
