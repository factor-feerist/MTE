#здесь код, получающий команды от интерфейса и передающий их client.py

import tkinter
import tkinter.messagebox
from tkinter.filedialog import asksaveasfile, askopenfile
from tkinter.messagebox import showerror

class Operations:
    def __init__(self, text, editor):
        self.text = text
        self.editor = editor

    def new_file(self):
        save_option = self.editor.ask_save_dialog()
        if save_option == "yes":
            self.save_file()
        elif save_option == "cancel":
            return

        self.editor.new_file()
        self.text.delete('1.0', tkinter.END)

    def open_file(self, file=None):
        self.text.delete('1.0', tkinter.END)
        for data in self.editor.open_file(file):
            self.text.insert(tkinter.END, data)

    def save_as(self):
        self.editor.save_as(data=self.text.get('1.0', tkinter.END))

    def save_file(self):
        self.editor.save_file(data=self.text.get('1.0', tkinter.END))

    def show_info(self):
        tkinter.messagebox.showinfo("Information", "Text Editor")

    def copy_text(self):
        selected_text = self.text.selection_get()
        if selected_text:
            self.text.clipboard_clear()
            self.text.clipboard_append(selected_text)

    def cut_text(self):
        selected_text = self.text.selection_get()
        if selected_text:
            self.text.delete(tkinter.SEL_FIRST, tkinter.SEL_LAST)
            self.text.clipboard_clear()
            self.text.clipboard_append(selected_text)

    def paste_text(self):
        clipboard_text = self.text.clipboard_get()
        if clipboard_text:
            self.text.insert(tkinter.INSERT, clipboard_text)
        self.text.update()


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

    def save_portion(self, content):
        file = open(self.inp.name, 'r+')
        file.seek(self.byte_numbers_array[self.pointer])

        if self.pointer != len(self.byte_numbers_array) - 1:
            self.byte_numbers_array[self.pointer + 1] = self.byte_numbers_array[self.pointer] + file.write(content) + 5
        else:
            self.byte_numbers_array.append(self.byte_numbers_array[self.pointer] + file.write(content) + 5)
        file.close()
