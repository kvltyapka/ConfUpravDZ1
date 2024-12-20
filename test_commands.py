import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
from main import create_gui, handle_command, ls, cd, chmod, clear, virtual_fs, current_path, current_user, computer_name

class TestVirtualOSCommands(unittest.TestCase):

    def setUp(self):
        global current_path
        current_path = ["God", "home"]

    def test_ls_command(self):
        output = ls(current_path)
        self.assertIn("user", output)
        self.assertIn("admin", output)

    def test_cd_command(self):
        global current_path
        current_path = ["God", "home"]
        cd(current_path, "user")
        self.assertEqual(current_path, ["God", "home", "user"])

        current_path = ["God", "home", "user"]
        cd(current_path, "..")
        self.assertEqual(current_path, ["God", "home"])

    def test_chmod_command(self):
        global current_path
        current_path = ["God", "home", "user"]
        chmod(current_path, "file1.txt", "755")
        self.assertEqual(virtual_fs["God"]["home"]["user"]["file1.txt"], "755")

    def test_clear_command(self):
        output_text = MagicMock()
        clear(output_text)
        output_text.delete.assert_called_with(1.0, tk.END)

    def test_unknown_command(self):
        output_text = MagicMock()
        handle_command("unknown_command", output_text)
        output_text.insert.assert_called_with(tk.END, "Unknown command\n")

if __name__ == "__main__":
    unittest.main()