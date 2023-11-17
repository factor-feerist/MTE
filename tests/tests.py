import sys
import os
import stat
from unittest import TestCase, main
sys.path.append('../')
from client.modules.edit_manager import EditManager
from server.modules.file_handler import FileHandler


def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)


class FileHandlerTests(TestCase):
    def setUp(self):
        self.handler = FileHandler()
        self.repository = f'{self.handler._current_directory}\\.rep'

    def tearDown(self):
        rmtree(self.repository)

    def test_new(self):
        self.handler.new('new', 'user1')
        self.assertTrue(os.path.isdir(f'{self.repository}\\files\\new'))
        self.assertTrue(os.path.exists(
            f'{self.repository}\\files\\new\\actual'))
        self.assertTrue(os.path.exists(f'{self.repository}\\files\\new'
                                       f'\\actual_version'))
        self.assertTrue(os.path.exists(f'{self.repository}\\files\\new\\log'))
        with open(f'{self.repository}\\users') as f:
            self.assertTrue('new\\\\user1\n' in f.read())

    def test_users_list(self):
        self.handler.new('abc', 'user1')
        self.handler.open('abc', 'user2')
        self.handler.new('abcd', 'user3')
        abc_users = self.handler.get_users_by_filename('abc')
        abcd_users = self.handler.get_users_by_filename('abcd')
        self.assertEqual(abc_users, ['user1', 'user2'])
        self.assertEqual(abcd_users, ['user3'])
        self.handler.remove_user_from_files('user1')
        abc_users = self.handler.get_users_by_filename('abc')
        self.assertEqual(abc_users, ['user2'])
        self.handler.remove_user_from_files('user2')
        abc_users = self.handler.get_users_by_filename('abc')
        self.assertEqual(abc_users, [])
        self.handler.remove_user_from_files('user3')
        abcd_users = self.handler.get_users_by_filename('abcd')
        self.assertEqual(abcd_users, [])

    def test_add(self):
        self.handler.new('add', 'user1')
        self.handler.open('add', 'user2')
        self.handler.add('add', 'user1', '0', 'abc')
        with open(f'{self.repository}\\files\\add\\actual') as f:
            self.assertEqual(f.read(), 'abc')
        self.handler.add('add', 'user2', '1', 'def')
        with open(f'{self.repository}\\files\\add\\actual') as f:
            self.assertEqual(f.read(), 'adefbc')

    def test_remove(self):
        self.handler.new('remove', 'user1')
        self.handler.open('remove', 'user2')
        self.handler.add('remove', 'user1', '0', 'abc')
        self.handler.add('remove', 'user2', '1', 'def')
        self.handler.remove('remove', 'user1', '1', 'd')
        with open(f'{self.repository}\\files\\remove\\actual') as f:
            self.assertEqual(f.read(), 'aefbc')
        self.handler.remove('remove', 'user2', '2', 'fb')
        with open(f'{self.repository}\\files\\remove\\actual') as f:
            self.assertEqual(f.read(), 'aec')

    def test_open(self):
        self.handler.new('open', 'user1')
        self.handler.add('open', 'user1', '0', 'abc')
        self.handler.add('open', 'user1', '1', 'def')
        self.handler.remove('open', 'user1', '1', 'de')
        text = self.handler.open('open', 'user2')
        self.assertEqual(text, 'afbc')

    def test_save(self):
        self.handler.new('save', 'user1')
        self.handler.add('save', 'user1', '0', 'abc')
        self.handler.open('save', 'user2')
        self.handler.save('save', 'user1')
        self.handler.remove('save', 'user2', '1', 'bc')
        with open(f'{self.repository}\\files\\save\\actual') as f:
            self.assertEqual(f.read(), 'a')
        with open(f'{self.repository}\\files\\save\\0') as f:
            self.assertEqual(f.read(), 'abc')
        self.handler.save('save', 'user2')
        self.handler.add('save', 'user1', '0', 'def')
        with open(f'{self.repository}\\files\\save\\actual') as f:
            self.assertEqual(f.read(), 'defa')
        with open(f'{self.repository}\\files\\save\\0') as f:
            self.assertEqual(f.read(), 'abc')
        with open(f'{self.repository}\\files\\save\\1') as f:
            self.assertEqual(f.read(), 'a')

    def test_watch(self):
        self.handler.new('watch', 'user1')
        self.handler.add('watch', 'user1', '0', 'abc')
        self.handler.open('watch', 'user2')
        self.handler.save('watch', 'user1')
        self.handler.remove('watch', 'user2', '1', 'bc')
        text = self.handler.watch('watch', 'actual')
        self.assertEqual(text, 'a')
        text = self.handler.watch('watch', '0')
        self.assertEqual(text, 'abc')
        self.handler.save('watch', 'user2')
        self.handler.add('watch', 'user1', '0', 'def')
        text = self.handler.watch('watch', 'actual')
        self.assertEqual(text, 'defa')
        text = self.handler.watch('watch', '0')
        self.assertEqual(text, 'abc')
        text = self.handler.watch('watch', '1')
        self.assertEqual(text, 'a')


class EditManagerTests(TestCase):
    def setUp(self):
        self.text_original = "new text made by me\n"\
                    "and my friend\n"\
                    "            - Stranger\n"
        self.file_name = "New File Special Name"
        self.username = "Anton"
        self.edit_manager = EditManager(self.text_original, None,
                                        self.file_name, self.username)

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
        edited_text = self.text_original[:10] + "pasted text" + \
                      self.text_original[10:]
        self.edit_manager.process_text_editing(edited_text)
        self.assertEqual(len(self.edit_manager.commands_queue), 1)
        self.assertEqual('a' == self.edit_manager.commands_queue[0][0], True)
        self.assertEqual(
            'pasted text' == self.edit_manager.commands_queue[0][-11:], True)

    def test_operations_select_and_add(self):
        edited_text = self.text_original[:27] + 'b' + self.text_original[33:]
        self.edit_manager.process_text_editing(edited_text)
        self.assertEqual(len(self.edit_manager.commands_queue), 2)
        self.assertEqual('r' == self.edit_manager.commands_queue[0][0], True)
        self.assertEqual(
            'friend' == self.edit_manager.commands_queue[0][-6:], True)
        self.assertEqual('a' == self.edit_manager.commands_queue[1][0], True)
        self.assertEqual('b' == self.edit_manager.commands_queue[1][-1], True)

    def test_operations_select_and_remove(self):
        edited_text = self.text_original[:27] + self.text_original[33:]
        self.edit_manager.process_text_editing(edited_text)
        self.assertEqual(len(self.edit_manager.commands_queue), 1)
        self.assertEqual('r' == self.edit_manager.commands_queue[0][0], True)
        self.assertEqual(
            'friend' == self.edit_manager.commands_queue[0][-6:], True)

    def test_operations_select_and_paste(self):
        edited_text = self.text_original[:27] + 'added text' + \
                      self.text_original[33:]
        self.edit_manager.process_text_editing(edited_text)
        self.assertEqual(len(self.edit_manager.commands_queue), 4)
        self.assertEqual('r' == self.edit_manager.commands_queue[0][0], True)
        self.assertEqual(
            'fri' == self.edit_manager.commands_queue[0][-3:], True)
        self.assertEqual('a' == self.edit_manager.commands_queue[2][0], True)
        self.assertEqual(
            'add' == self.edit_manager.commands_queue[2][-3:], True)


if __name__ == "__main__":
    main()
