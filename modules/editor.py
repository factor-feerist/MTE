import tkinter
from tkinter.filedialog import asksaveasfile, askopenfile
from tkinter.messagebox import showerror


class Editor:
    def __init__(self):
        self.file_name = tkinter.NONE
        self.byte_numbers_array = [0]
        self.pointer = -1
        self.inp = None
        self.content = ""

    def ask_save_dialog(self):
        result = tkinter.messagebox.askyesnocancel(title="Save File", message="Do you want to save the current file?")
        if result is True:
            return "yes"
        elif result is False:
            return "no"
        else:
            return "cancel"

    def new_file(self):
        self.file_name = "Untitled"

    def save_file(self, data):
        try:
            out = open(self.file_name, 'w')
        except FileNotFoundError:
            out = open(self.file_name, 'x')
        out.write(data)
        out.close()

    def save_as(self, data):
        out = asksaveasfile(mode='w', defaultextension='txt')
        try:
            out.write(data.rstrip())
        except Exception:
            showerror(title="Error", message="Saving file error")

    def open_file(self, file=None):
        if file is None:
            self.inp = askopenfile(mode="r+")
        else:
            self.inp = open(file, mode="r+")
        if self.inp is None:
            return
        self.file_name = self.inp.name
        for i in range(5):
            yield self.inp.readline()
        self.byte_numbers_array.append(self.inp.tell())
        self.pointer += 1
