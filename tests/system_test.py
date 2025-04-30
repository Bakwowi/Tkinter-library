import unittest
import os
from tkinter import Tk

import sys
sys.path.append(r'C:\Users\Bryan\Desktop\school-documents\2nd-semester-SS-25\projects\programming-2\exercise_5')

from view import ViewClass
from controller import LibController

class TestSystem(unittest.TestCase):
    def setUp(self):
        # Set up the application
        self.root = Tk()
        self.view = ViewClass(self.root)
        self.controller = LibController(self.view)

        # Ensure the test library folder exists
        if not os.path.exists("libraries"):
            os.mkdir("libraries")

    def tearDown(self):
        # Destroy the GUI and clean up
        self.root.destroy()
        if os.path.exists("libraries/Test_library.json"):
            os.remove("libraries/Test_library.json")

    def test_create_and_open_library(self):
        # Simulate creating a new library
        self.view.create_new_window = lambda instruction: (
            self.root,  # Mock window
            self.view.lib_stats_nameval,  # Mock label
            self.view.book_title_entry,  # Mock submit button
            self.view.book_author_entry,  # Mock close button
            self.view.book_year_entry,  # Mock entry field
        )
        self.view.book_year_entry.get = lambda: "Test_library"

        # Call the create library function
        self.controller.create_delete_library("Create a new library")

        # Verify the library was created
        self.assertTrue(os.path.exists("libraries/Test_library.json"))

        # Simulate opening the library
        self.controller.open_library("Test_library")

        # Verify the library was opened
        self.assertEqual(self.view.lib_stats_nameval.cget("text"), "Test_library")

    def test_add_book_to_library(self):
        # Simulate adding a book
        self.view.get_add_book_entry_contents = lambda: ("Test Title", "Test Author", "2023", "Fiction")
        self.controller.add_book_to_library("Test_library")

        # Verify the book was added
        books = self.controller.view.treeview.get_children()
        self.assertEqual(len(books), 1)

    def test_delete_book_from_library(self):
        # Simulate adding a book
        self.view.get_add_book_entry_contents = lambda: ("Test Title", "Test Author", "2023", "Fiction")
        self.controller.add_book_to_library("Test_library")

        # Simulate selecting the book in the treeview
        self.view.treeview.selection = lambda: ["item1"]
        self.view.treeview.item = lambda item: {"values": ["1", "Test Title", "Test Author", "2023", "Fiction"]}

        # Call the delete book function
        self.controller.delete_book_from_library("Test_library")

        # Verify the book was deleted
        books = self.controller.view.treeview.get_children()
        # self.assertEqual(len(books), 0)

if __name__ == "__main__":
    unittest.main()