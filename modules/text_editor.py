#здесь код, получающий команды от интерфейса и передающий их client.py
import difflib
import tkinter
import tkinter.messagebox
from tkinter.filedialog import asksaveasfile, askopenfile
from tkinter.messagebox import showerror

class Operations:
    def __init__(self, text, editor, server):
        self.text = text
        self.prev_text_as_line = self.text.get("1.0", tkinter.END)
        self.server = server
        self.differ = difflib.Differ()
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

    def send_remove_commands(self, to_remove):
        for element in to_remove:
            command = f"- [{element[1]}] ; pos [{element[0]}]"
            self.server.send(command)

    def send_add_commands(self, to_add):
        for element in to_add:
            command = f"+ [{element[1]}] ; pos [{element[0]}]"
            self.server.send(command)

    def handle_texts_difference(self):
        text_line = self.text.get("1.0", tkinter.END)
        to_add, to_remove = self.find_difference_in_texts(text_line, self.prev_text_as_line)
        self.send_remove_commands(to_remove)
        self.send_add_commands(to_add)
        self.prev_text_as_line = text_line[:]

    def get_text_edits_list(self, diff, edit_mark):
        result = []
        index = 0
        for symbol in diff:
            if symbol[0] == edit_mark:
                if len(result) > 0 and result[-1][0] + len(result[-1][1]) == index:
                    sequence_index = result[-1][0]
                    sequence_value = result[-1][1]
                    result[-1] = (sequence_index, sequence_value + symbol[2])
                else:
                    result.append((index, symbol[2]))
            index += 1 if symbol[0] == edit_mark or symbol[0] == ' ' else 0
        return result

    def find_difference_in_texts(self, text1, text2):
        diff = self.differ.compare(rf"{text2}", rf"{text1}")
        diff2 = self.differ.compare(rf"{text2}", rf"{text1}")
        to_add = self.get_text_edits_list(diff, '+')
        to_remove = self.get_text_edits_list(diff2, '-')
        return to_add, to_remove

    def process_keyboard_event(self, event):
        pressed_key = event.keysym
        if pressed_key in ["Control_L", "Alt_L", "Shift_L"]:
            return
        self.handle_texts_difference()


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
