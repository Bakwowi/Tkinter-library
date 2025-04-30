import unittest
from unittest.mock import MagicMock, patch
import sys

sys.path.append(r'C:\Users\Bryan\Desktop\school-documents\2nd-semester-SS-25\projects\programming-2\exercise_5')
from controller import LibController
from model import *
import os

class TestLibControllerIntegration(unittest.TestCase):
    def setUp(self):
        # Mock the view
        self.mock_view = MagicMock()
        self.controller = LibController(self.mock_view)
        self.controller.authenticate_entries = MagicMock()
        self.controller.update_message_box = MagicMock()
        self.controller.refresh_library = MagicMock()
        self.controller.update_treeview = MagicMock()
        self.controller.stop_event = MagicMock()

        # Set up a test library
        self.test_library_name = "Test_library"
        clear_library(self.test_library_name)  # Ensure the library is empty before each test

    def tearDown(self):
        # Clear the test library after each test
        clear_library(self.test_library_name)
        # Remove the test library file if it exists
        if os.path.exists(f"libraries/{self.test_library_name}.json"):
            os.remove(f"libraries/{self.test_library_name}.json")


    # @patch("model.add_book")
    def test_add_book_to_library_success(self):
        # Mock user input from the view
        self.mock_view.get_add_book_entry_contents.return_value = ("Test Title", "Test Author", "2023", "Fiction")
        self.controller.authenticate_entries.return_value = ["All Good", "success"]

        # Mock the add_book function to return success
        with patch("controller.add_book") as mock_add_book:
            mock_add_book.return_value = ["Book added successfully.", "success"]

            self.controller.update_message_box.reset_mock()

            # Call the function
            self.controller.add_book_to_library(self.test_library_name)
            
            # Assertions
            self.mock_view.get_add_book_entry_contents.assert_called_once()
            self.controller.authenticate_entries.assert_called_once()
            self.controller.update_message_box.assert_any_call(["Book added successfully.", "success"], self.test_library_name)
            mock_add_book.assert_called_once()

    def test_add_book_to_library_failure(self):
        self.mock_view.get_add_book_entry_contents.return_value = ["", "", "", ""]

        with patch("controller.add_book") as mock_add_book:
            self.controller.authenticate_entries.return_value = ["Please fill in all the add-book entries", "danger"]

            self.controller.update_message_box.reset_mock()

            # Call the function
            self.controller.add_book_to_library(self.test_library_name)
           
            # Assertions
            self.mock_view.get_add_book_entry_contents.assert_called_once()   
            self.controller.authenticate_entries.assert_called_once()
            self.controller.update_message_box.assert_any_call(["Please fill in all the add-book entries", "danger"], self.test_library_name)
            mock_add_book.assert_not_called()

    def test_search_book_from_library(self):
        self.mock_view.get_search_book_entry_contents.return_value = ["Test Title", "", "", ""]
        self.controller.authenticate_entries.return_value = ["All Good", "success"]

        with patch("controller.search_book") as mock_search_book:
            mock_search_book.return_value = ["Book(s) successfully found", "success"]

            self.controller.update_message_box.reset_mock()

            # Call the function
            self.controller.search_book_from_library(self.test_library_name)
            
            # Assertions
            self.mock_view.get_search_book_entry_contents.assert_called_once()
            self.controller.authenticate_entries.assert_called_once()
            self.controller.update_message_box.assert_called_once()
            mock_search_book.assert_called_once()

    def test_search_book_from_library_failure(self):
        self.mock_view.get_search_book_entry_contents.return_value = ["", "", "", ""]

        with patch("controller.search_book") as mock_search_book:
            self.controller.authenticate_entries.return_value = ["Please fill in all the search-book entries", "danger"]

            self.controller.update_message_box.reset_mock()

            # Call the function
            self.controller.search_book_from_library(self.test_library_name)
            
            # Assertions
            self.mock_view.get_search_book_entry_contents.assert_called_once()
            self.controller.authenticate_entries.assert_called_once()
            self.controller.update_message_box.assert_any_call(["Please fill in all the search-book entries", "danger"], self.test_library_name)
            mock_search_book.assert_not_called()

    def test_delete_book_from_library_success(self):
       
        # Mock the treeview selection
        self.mock_view.treeview.selection.return_value = ["item1"]
        self.mock_view.treeview.item.return_value = {"values": ["1", "Test Title", "Test Author", "2023", "Fiction"]}

        with patch("controller.delete_book") as mock_delete_book:

             # Mock the delete_book function to return success
            mock_delete_book.return_value = ["Book(s) deleted successfully.", "success"]
            # Call the function
            self.controller.delete_book_from_library(self.test_library_name)

            # Assertions
            self.mock_view.treeview.selection.assert_called_once()  # Ensure selection was retrieved
            self.mock_view.treeview.item.assert_called_once_with("item1")  # Ensure item details were retrieved
            mock_delete_book.assert_called_once_with("Test Title", self.test_library_name)  # Ensure delete_book was called
            self.controller.update_treeview.assert_called_once_with(self.test_library_name)  # Ensure treeview was updated
            self.controller.update_message_box.assert_any_call(["Book(s) deleted successfully.", "success"], self.test_library_name)  # Ensure success message was shown

    def test_delete_book_from_library_no_selection(self):
        # Mock the treeview selection to return no items
        self.mock_view.treeview.selection.return_value = []

        # Call the function
        self.controller.delete_book_from_library(self.test_library_name)

        # Assertions
        self.mock_view.treeview.selection.assert_called_once()  # Ensure selection was retrieved
        self.controller.update_message_box.assert_any_call(["Please select a book first", "danger"], self.test_library_name)  # Ensure error message was shown

    def test_clear_all_books_from_library(self):
    
        with patch("controller.clear_library") as mock_clear_library:
            mock_clear_library.return_value = ["The library has been successfully cleared.", "success"]

            # Call the function
            self.controller.clear_all_books_from_library(self.test_library_name)

            # Assertions
            mock_clear_library.assert_called_once_with(self.test_library_name)
            self.controller.update_treeview.assert_called_once_with(self.test_library_name)
            self.controller.update_message_box.assert_any_call(["The library has been successfully cleared.", "success"], self.test_library_name)

    def test_list_libraries(self):
        with patch("controller.os.listdir") as mock_listdir:
            # Mock the os.listdir function
            mock_listdir.return_value = ["Default_library.json", "Test_library.json"]

            # Call the function
            self.controller.list_libraries()

            # Assertions
            mock_listdir.assert_called_once_with("libraries")
            self.mock_view.menu_libraries.delete.assert_any_call(0, "end")
            # self.mock_view.menu_libraries.insert_command.assert_any_call(0, label="Default_library", command=MagicMock())
            # self.mock_view.menu_libraries.add_command.assert_any_call(label="Test_library", command=MagicMock())

    def test_open_library(self):
        with patch("controller.json.load") as mock_json_load:
            with patch("controller.open") as mock_open:
                # Mock the open and json.load functions
                mock_open.return_value.__enter__.return_value = MagicMock()
                mock_json_load.return_value = []

                # Call the function
                self.controller.open_library(self.test_library_name)

                # Assertions
                mock_open.assert_called_once_with(f"libraries/{self.test_library_name}.json", "r")
                mock_json_load.assert_called_once()
                self.controller.refresh_library.assert_any_call(self.test_library_name, "clear_message_box")
                self.controller.update_message_box.assert_any_call(
                    [f"{self.test_library_name} has been opened.", "success"], self.test_library_name)

    def test_sort_library(self):
        with patch("controller.sort_books") as mock_sort_books:
            # Mock the sort_books function
            mock_sort_books.return_value = ["Books sorted successfully.", "success"]

            # Simulate user input
            self.mock_view.sort_book_entry.get.return_value = "title"

            # Call the function
            self.controller.sort_library(self.test_library_name)

            # Assertions
            mock_sort_books.assert_called_once_with("title", self.test_library_name)
            self.controller.update_treeview.assert_called_once_with(self.test_library_name)
            self.controller.update_message_box.assert_any_call(["Books sorted successfully.", "success"], self.test_library_name)

    


     
if __name__ == "__main__":
    unittest.main()