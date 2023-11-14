# здесь интерфейс самого текстового редактора
import tkinter
from tkinter.messagebox import showinfo
from tkinter import Tk, Label, Text, Scrollbar, Menu, VERTICAL, END


class Gui:
    def __init__(self, edit_manager, text, file_name, username, edit=True):
        self.window = Tk()
        self.window.title(f"Text editor --- {file_name} --- {username}")
        if edit:
            self.text = Text(self.window, width=400, height=400, wrap="word")
            self.text.insert('1.0', text)
            self.scrollbar = Scrollbar(self.window, orient=VERTICAL, command=self.text.yview)
            self.setup_scrollbar()
            self.setup_text()
        else:
            self.label = Label(self.window, width=400, height=400, text=text, anchor=tkinter.NW)
            self.label.pack()
        self.operations = edit_manager
        self.file_name = file_name
        self.username = username
        self.menu = Menu(self.window)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.setup_window()
        # self.setup_file_menu()
        self.setup_menu()
        self.setup_key_bindings()

    def setup_window(self):
        self.window.minsize(width=500, height=500)
        self.window.maxsize(width=500, height=500)
        self.window.config(menu=self.menu)

    def setup_text(self):
        self.text.configure(yscrollcommand=self.scrollbar.set)
        self.text.pack()

    def setup_scrollbar(self):
        self.scrollbar.pack(side="right", fill="y")

    # def setup_file_menu(self):
    #     self.file_menu.add_command(label="Save file", command=self.operations.save_file)

    def setup_key_bindings(self):
        self.window.bind("<Key>", self.handle_editing_in_text)

    def handle_editing_in_text(self, event):
        pressed_key = event.keysym
        if pressed_key not in ["Control_L", "Alt_L", "Shift_L"]:
            self.operations.process_text_editing(self.text.get("1.0", END))

    def setup_menu(self):
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="Info", command=lambda: showinfo("Information", "Text Editor"))

    def run(self):
        self.window.mainloop()
