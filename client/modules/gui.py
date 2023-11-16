import tkinter
from tkinter.messagebox import showinfo
from tkinter import Tk, Label, Text, Scrollbar, Menu, VERTICAL, END


class Gui:
    def __init__(self, edit_manager, text, file_name, username, edit=True):
        self.window = Tk()
        self.window.title(f"Text editor --- {file_name} --- {username}")
        self.edit = edit
        self.text = Text(self.window, width=400, height=400, wrap="word")
        self.text.insert('1.0', text)
        self.scrollbar = Scrollbar(self.window, orient=VERTICAL, command=self.text.yview)
        self.setup_scrollbar()
        self.setup_text()
        self.operations = edit_manager
        self.file_name = file_name
        self.username = username
        self.menu = Menu(self.window)
        self.setup_window()
        self.setup_menu()
        self.setup_key_bindings()
        self.is_closed = False
        self.save_is_pressed = False
        self.window.protocol("WM_DELETE_WINDOW", self.switch_close_flag)

    def switch_close_flag(self):
        self.is_closed = True
        self.window.quit()

    def switch_save_flag(self):
        self.save_is_pressed = True

    def setup_window(self):
        self.window.minsize(width=500, height=500)
        self.window.maxsize(width=500, height=500)
        self.window.config(menu=self.menu)

    def setup_text(self):
        self.text.configure(yscrollcommand=self.scrollbar.set)
        self.text.pack()

    def setup_scrollbar(self):
        self.scrollbar.pack(side="right", fill="y")

    def setup_key_bindings(self):
        self.window.bind("<Key>", self.handle_editing_in_text)

    def handle_editing_in_text(self, event):
        pressed_key = event.keysym
        if pressed_key not in ["Control_L", "Alt_L", "Shift_L"] and self.edit:
            self.operations.process_text_editing(self.text.get("1.0", END))

    def setup_menu(self):
        if self.edit:
            self.menu.add_cascade(label="Save", command=self.switch_save_flag)
        self.menu.add_cascade(label="Info", command=lambda: showinfo("Information", "Text Editor"))

    def update_text(self, text, operations_handler):
        self.text.delete("1.0", tkinter.END)
        self.text.insert(tkinter.END, text)
        operations_handler.prev_text = operations_handler.text
        operations_handler.text = text

    def run(self):
        self.window.mainloop()
