import unittest
from unittest.mock import MagicMock, patch
import os
import json
from model import *


class TestModel(unittest.TestCase):
    def setUp(self):
        # Set up a test library file
        self.test_library_name = "Test_library"
        self.test_library_path = f"libraries/{self.test_library_name}.json"
        if not os.path.exists("libraries"):
            os.mkdir("libraries")
        with open(self.test_library_path, "w") as file:
            json.dump([], file)

    def tearDown(self):
        # Clean up the test library file after each test
        if os.path.exists(self.test_library_path):
            os.remove(self.test_library_path)

    def test_get_library_success(self):
        library = get_library(self.test_library_name)
        self.assertIsInstance(library, list)

    def test_update_library_success(self):
        new_book = {
            "title": "Test Title",
            "author": "Test Author",
            "year": 2023,
            "genre": "Fiction"
        }
        library = get_library(self.test_library_name)
        library.append(new_book)
        update_library(library, self.test_library_name)
        updated_library = get_library(self.test_library_name)
        self.assertEqual(len(updated_library), 1)
        self.assertEqual(updated_library[0]["title"], "Test Title")
        self.assertEqual(updated_library[0]["author"], "Test Author")
        self.assertEqual(updated_library[0]["year"], 2023)
        self.assertEqual(updated_library[0]["genre"], "Fiction")

    def test_get_number_of_books_success(self):
        num_books = get_num_books(self.test_library_name)
        self.assertEqual(num_books, 0)

        new_book = {
            "title": "Test Title",
            "author": "Test Author",
            "year": 2023,
            "genre": "Fiction"
        }
        library = get_library(self.test_library_name)
        library.append(new_book)
        update_library(library, self.test_library_name)
        new_num_books = get_num_books(self.test_library_name)
        self.assertEqual(new_num_books, 1)

    def test_add_book_success(self):
        # Test adding a valid book
        result = add_book("Test Title", "Test Author", "2023", "Fiction", self.test_library_name)
        self.assertEqual(result, ["Book added successfully.", "success"])
        library = get_library(self.test_library_name)
        self.assertEqual(len(library), 1)
        self.assertEqual(library[0]["title"], "Test Title")
        self.assertEqual(library[0]["author"], "Test Author")
        self.assertEqual(library[0]["year"], 2023)
        self.assertEqual(library[0]["genre"], "Fiction")

    def test_add_book_duplicate(self):
        # Test adding a duplicate book
        add_book("Test Title", "Test Author", "2023", "Fiction", self.test_library_name)
        result = add_book("Test Title", "Test Author", "2023", "Fiction", self.test_library_name)
        self.assertEqual(result, ["This book already exists.", "danger"])

    def test_add_book_invalid_year(self):
        # Test adding a book with an invalid year
        result = add_book("Test Title", "Test Author", "InvalidYear", "Fiction", self.test_library_name)
        self.assertEqual(result, ["Invalid year. Please enter a valid number for the year.", "danger"])

    def test_add_book_empty_fields(self):
        # Test adding a book with empty fields
        result = add_book("", "", "", "", self.test_library_name)
        self.assertEqual(result, ["Invalid year. Please enter a valid number for the year.", "danger"])

    def test_delete_book_success(self):
        
        # Test deleting a book
        add_book("Test Title", "Test Author", "2023", "Fiction", self.test_library_name)
        result = delete_book("Test Title", self.test_library_name)
        self.assertEqual(result, ["Book(s) deleted successfully.", "success"])
        library = get_library(self.test_library_name)
        self.assertEqual(len(library), 0)

    def test_delete_book_not_found(self):
            # Test deleting a book that doesn't exist
            add_book("Test Title", "Test Author", "2023", "Fiction", self.test_library_name)
            result = delete_book("Nonexistent Book", self.test_library_name)
            self.assertEqual(result, ["Book not found", "danger"])

    def test_search_book_success(self):
        # Test searching for a book
        add_book("Test Title", "Test Author", "2023", "Fiction", self.test_library_name)
        result = search_book("Test Title", "", "", "", self.test_library_name)
        self.assertEqual(result[1], ["Book(s) successfully found", "success"])
        self.assertEqual(len(result[0]), 1)
        # print(result[0])
        self.assertEqual(result[0][0][1], "Test Title")
    
    def test_search_book_not_found(self):
        # Test searching for a book that doesn't exist
        add_book("Test Title", "Test Author", "2023", "Fiction", self.test_library_name)
        result = search_book("Nonexistent Book", "", "", "", self.test_library_name)
        self.assertEqual(result[1], ["Book not found", "danger"])
        self.assertEqual(len(result[0]), 0)
    
    def test_list_books_success(self):
        add_book("Test Title", "Test Author", "2023", "Fiction", self.test_library_name)
        add_book("Another Title", "Another Author", "2022", "History", self.test_library_name)
        result = list_books(self.test_library_name)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0][1], "Test Title")
        self.assertEqual(result[0][1][1], "Another Title")
    
    def test_list_books_empty(self):
        # Test listing books when the library is empty
        result = list_books(self.test_library_name)
        self.assertEqual(result, ["The library is empty. No books to list.", "danger"])

    def test_sort_books_success(self):
        add_book("Test Title", "Test Author", "2023", "Fiction", self.test_library_name)
        add_book("Another Title", "Another Author", "2022", "History", self.test_library_name)
        result = sort_books("title", self.test_library_name)
        self.assertEqual(result[0], "All the books have been successfully sorted")
        self.assertEqual(result[1], "success")

        library = get_library(self.test_library_name)
        self.assertEqual(library[0]["title"], "Another Title")
        self.assertEqual(library[1]["title"], "Test Title")

    def test_sort_books_invalid_key(self):
        # Test sorting books with an invalid key
        add_book("Test Title", "Test Author", "2023", "Fiction", self.test_library_name)
        result = sort_books("invalid_key", self.test_library_name)
        self.assertEqual(result[0], "Invalid sorting key. Please use 'title', 'author', 'year', or 'genre'.")
        self.assertEqual(result[1], "danger")
    
    def test_sort_books_empty(self):
        # Test sorting books when the library is empty
        result = sort_books("title", self.test_library_name)
        self.assertEqual(result[0], "The library is empty. No books to sort.")
        self.assertEqual(result[1], "danger")

    def test_clear_library_success(self):
        # Test clearing the library
        add_book("Test Title", "Test Author", "2023", "Fiction", self.test_library_name)
        add_book("Another Title", "Another Author", "2024", "History", self.test_library_name)

        result = clear_library(self.test_library_name)
        self.assertEqual(result, ["The library has been successfully cleared.", "success"])
        library = get_library(self.test_library_name)
        self.assertEqual(len(library), 0)
    
    def test_create_library_success(self):
        # Test creating a new library
        new_library_name = "New_Library"
        result = create_delete_library_execute(new_library_name, "create")
        self.assertEqual(result, ["New_Library has been successfully created", "success"])
        library = get_library(new_library_name)
        self.assertIsInstance(library, list)
        os.remove(f"libraries/{new_library_name}.json")

    def test_create_library_already_exists(self):
        # Test creating a library that already exists
        new_library_name = "Test_library"
        result = create_delete_library_execute(new_library_name, "create")
        self.assertEqual(result, ["The library you want to create already exists", "danger"])

    def test_delete_library_success(self):
        new_library_name = "Test_library"
        create_delete_library_execute(new_library_name, "create")

        result = create_delete_library_execute(new_library_name, "delete")
        self.assertEqual(result[0], "Test_library has been successfully deleted")

    def test_delete_library_not_fount(self):
        new_library_name = "Another_Library"
        result = create_delete_library_execute(new_library_name, "delete")
        self.assertEqual(result[0], "Library not found.")

    @patch("model.add_book")
    def test_create_mill_books_success(self, mock_add_book):
        # Mock the add_book function to always return success
        mock_add_book.return_value = ["Book added successfully", "success"]

        # Mock UI elements
        mock_stop_event = MagicMock()
        mock_stop_event.is_set.return_value = False

        mock_progress_bar = MagicMock()
        mock_new_window = MagicMock()
        mock_label = MagicMock()
        mock_treeview = MagicMock()

        # Call the function
        result = create_mill_books(mock_stop_event, mock_progress_bar, mock_new_window, mock_label, mock_treeview, self.test_library_name)

        # Assertions
        self.assertEqual(result, "1000 books successfully created")
        self.assertEqual(mock_add_book.call_count, 1000)  # Ensure add_book was called 10 times
        mock_progress_bar.__setitem__.assert_called()  # Ensure progress bar was updated
        mock_treeview.insert.assert_called()  # Ensure treeview was updated

    @patch("model.add_book")
    def test_create_mill_books_cancelled(self, mock_add_book):
        # Mock the add_book function
        mock_add_book.return_value = ["Book added successfully", "success"]

        # Mock UI elements
        mock_stop_event = MagicMock()
        mock_stop_event.is_set.side_effect = [False, False, True]  # Simulate cancellation after 2 iterations

        mock_progress_bar = MagicMock()
        mock_new_window = MagicMock()
        mock_label = MagicMock()
        mock_treeview = MagicMock()

        # Call the function
        result = create_mill_books(mock_stop_event, mock_progress_bar, mock_new_window, mock_label, mock_treeview, self.test_library_name)

        # Assertions
        self.assertEqual(result, "Book creation was cancelled.")
        self.assertLess(mock_add_book.call_count, 1000)  # Ensure add_book was not called 10 times
        mock_progress_bar.__setitem__.assert_called()  # Ensure progress bar was updated

        
        

if __name__ == "__main__":
    unittest.main()
