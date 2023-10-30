#здесь интерфейс самого текстового редактора

import tkinter
from tkinter import Scrollbar, VERTICAL
from modules import text_editor


class Gui:
    def __init__(self):
        self.window = tkinter.Tk()
        self.text = tkinter.Text(self.window, width=400, height=400, wrap="word")
        self.scrollbar = Scrollbar(self.window, orient=VERTICAL, command=self.text.yview)
        self.editor = text_editor.Editor()
        self.operations = text_editor.Operations(self.text, self.editor)
        self.menu = tkinter.Menu(self.window)
        self.file_menu = tkinter.Menu(self.menu, tearoff=0)
        self.edit_menu = tkinter.Menu(self.menu, tearoff=0)
        self.setup_window()
        self.setup_scrollbar()
        self.setup_text()
        self.setup_file_menu()
        self.setup_edit_menu()
        self.setup_menu()
        self.setup_shortcuts()

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
        self.file_menu.add_command(label="New", command=self.operations.new_file)
        self.file_menu.add_command(label="Open", command=self.operations.open_file)
        self.file_menu.add_command(label="Save file", command=self.operations.save_file)
        self.file_menu.add_command(label="Save as", command=self.operations.save_as)

    def setup_edit_menu(self):
        self.edit_menu.add_command(label="Copy", command=self.operations.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.operations.paste_text)
        self.edit_menu.add_command(label="Cut", command=self.operations.cut_text)

    def setup_shortcuts(self):
        self.window.bind("<Control-n>", self.editor.new_file)
        self.window.bind("<Control-o>", self.editor.open_file)
        self.window.bind("<Control-s>", self.editor.save_file)
        self.window.bind("<Alt-s>", self.editor.save_as)

    def setup_menu(self):
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu.add_cascade(label="Info", command=self.operations.show_info)

    def run(self):
        self.window.mainloop()
