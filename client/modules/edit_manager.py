# здесь код, получающий команды от интерфейса и передающий их client.py
from difflib import Differ


class EditManager:
    def __init__(self, text_as_string, server, file_name, username):
        self.text = text_as_string
        self.prev_text = text_as_string
        self.server = server
        self.differ = Differ()
        self.file_name = file_name
        self.username = username
        self.commands_queue = []

    def process_text_editing(self, edited_text):
        self.prev_text = self.text
        self.text = edited_text
        self.handle_texts_difference()

    def handle_texts_difference(self):
        to_add, to_remove = self.find_difference_in_texts()
        self.enqueue_remove_commands(to_remove)
        self.enqueue_add_commands(to_add)

    def find_difference_in_texts(self):
        diff_1 = self.differ.compare(rf"{self.prev_text}", rf"{self.text}")
        diff_2 = self.differ.compare(rf"{self.prev_text}", rf"{self.text}")
        to_add = self.get_text_edits_list(diff_1, '+')
        to_remove = self.get_text_edits_list(diff_2, '-')
        return to_add, to_remove

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

    def enqueue_remove_commands(self, to_remove):
        for element in to_remove:
            command = f"r {self.file_name}\\\\{self.username}\\\\{element[0]}\\\\{element[1]}"
            self.commands_queue.append(command)

    def enqueue_add_commands(self, to_add):
        for element in to_add:
            command = f"a {self.file_name}\\\\{self.username}\\\\{element[0]}\\\\{element[1]}"
            self.commands_queue.append(command)

    def get_next_command(self):
        if len(self.commands_queue) > 0:
            return self.commands_queue.pop(0)
        return ""
