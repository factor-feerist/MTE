from unittest import TestCase
from client.modules.edit_manager import EditManager

class Tests(TestCase):
    def setUp(self):
        self.text_original = "new text made by me\n"\
                    "and my friend\n"\
                    "            - Stranger\n"
        self.file_name = "New File Special Name"
        self.username = "Anton"
        self.edit_manager = EditManager(self.text_original, None, self.file_name, self.username)

    def test_operations_add(self):
        edited_text = self.text_original[:10] + 'b' + self.text_original[10:]
        self.edit_manager.process_text_editing(edited_text)
        self.assertEqual(len(self.edit_manager.commands_queue), 1)
        self.assertEqual('a' == self.edit_manager.commands_queue[0][0], True)
        self.assertEqual('b' == self.edit_manager.commands_queue[0][-1], True)

    def test_operations_remove(self):
        edited_text = self.text_original[:9] + self.text_original[10:]
        self.edit_manager.process_text_editing(edited_text)
        self.assertEqual(len(self.edit_manager.commands_queue), 1)
        self.assertEqual('r' == self.edit_manager.commands_queue[0][0], True)
        self.assertEqual('m' == self.edit_manager.commands_queue[0][-1], True)

    def test_operations_paste(self):
        edited_text = self.text_original[:10] + "pasted text" + self.text_original[10:]
        self.edit_manager.process_text_editing(edited_text)
        self.assertEqual(len(self.edit_manager.commands_queue), 1)
        self.assertEqual('a' == self.edit_manager.commands_queue[0][0], True)
        self.assertEqual('pasted text' == self.edit_manager.commands_queue[0][-11:], True)

    def test_operations_select_and_add(self):
        edited_text = self.text_original[:27] + 'b' + self.text_original[33:]
        self.edit_manager.process_text_editing(edited_text)
        self.assertEqual(len(self.edit_manager.commands_queue), 2)
        self.assertEqual('r' == self.edit_manager.commands_queue[0][0], True)
        self.assertEqual('friend' == self.edit_manager.commands_queue[0][-6:], True)
        self.assertEqual('a' == self.edit_manager.commands_queue[1][0], True)
        self.assertEqual('b' == self.edit_manager.commands_queue[1][-1], True)

    def test_operations_select_and_remove(self):
        edited_text = self.text_original[:27] + self.text_original[33:]
        self.edit_manager.process_text_editing(edited_text)
        self.assertEqual(len(self.edit_manager.commands_queue), 1)
        self.assertEqual('r' == self.edit_manager.commands_queue[0][0], True)
        self.assertEqual('friend' == self.edit_manager.commands_queue[0][-6:], True)

    def test_operations_select_and_paste(self):
        edited_text = self.text_original[:27] + 'added text' + self.text_original[33:]
        self.edit_manager.process_text_editing(edited_text)
        self.assertEqual(len(self.edit_manager.commands_queue), 4)
        self.assertEqual('r' == self.edit_manager.commands_queue[0][0], True)
        self.assertEqual('fri' == self.edit_manager.commands_queue[0][-3:], True)
        self.assertEqual('a' == self.edit_manager.commands_queue[2][0], True)
        self.assertEqual('add' == self.edit_manager.commands_queue[2][-3:], True)
