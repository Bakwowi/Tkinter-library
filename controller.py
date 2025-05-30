import threading
import os
import json
from model import *

# Ensure the "libraries" folder and the default library file exist
if not os.path.exists("libraries"):
    os.mkdir("libraries")
if not os.path.exists("libraries/Default_library.json"):
    with open("libraries/Default_library.json", "w") as file:
        json.dump([], file)

# Global variable to track the currently opened library
currently_opened_library = "Default_library"

# Event to signal stopping threads
stop_event = threading.Event()

class LibController:
    def __init__(self, viewclass):
        # Initialize the controller with the view class
        self.view = viewclass
        
        # Configure menu and button commands
        self.view.menu_file.entryconfig(0, command=lambda: self.create_delete_library("Create a new library"))
        self.view.menu_file.entryconfig(2, command=lambda: self.create_delete_library("Delete a library"))
        self.view.menu_file.entryconfig(4, command=lambda: self.create_million_books(currently_opened_library))
        
        self.view.add_book_button.config(command=lambda: self.add_book_to_library(currently_opened_library))
        self.view.search_button.config(command=lambda: self.search_book_from_library(currently_opened_library))
        self.view.delete_book_button.config(command=lambda: self.delete_book_from_library(currently_opened_library))
        self.view.clear_all_books_button.config(command=lambda: self.clear_all_books_from_library(currently_opened_library))
        self.view.refresh_button.config(command=lambda: self.refresh_library(currently_opened_library, "clear_message_box"))
        self.view.sort_book_button.config(command=lambda: self.sort_library(currently_opened_library))
        self.view.search_image_button.config(command=lambda: self.search_book_with_image(currently_opened_library))

        # Start threads for listing libraries and opening the default library
        self.handle_threading(self.list_libraries)
        self.handle_threading(self.open_library, "Default_library")

    # Function to authenticate user input for adding or searching books
    def authenticate_entries(self, title_entry, author_entry, year_entry, genre_entry, add_or_search):
        if add_or_search == "add":
            if title_entry.strip() == "" or author_entry.strip() == "" or year_entry.strip() == "" or genre_entry.strip() == "":
                return ["Please fill in all the add-book entries", "danger"]
            else:
                return ["All Good", "success"]
        elif add_or_search == "search":
            if title_entry.strip() == "" and author_entry.strip() == "" and year_entry.strip() == "" and genre_entry.strip() == "":
                return ["Please fill in all the search-book entries", "danger"]
            else:
                return ["All Good", "success"]

    # Function to update the message box in the view
    def update_message_box(self, message, library):
        if message[1] == "danger":
            return self.view.show_message(message, library)
        elif message[1] == "success":
            return self.view.show_message(message, library)

    # Function to add a book to the library
    def add_book_to_library(self, library):
        book_details = self.view.get_add_book_entry_contents()
        title, author, year, genre = book_details
        authenticate_entries = self.authenticate_entries(title, author, year, genre, "add")
        if "success" in authenticate_entries:
            response = add_book(title, author, year, genre, library)
            if "success" in response:
                self.refresh_library(library)
                return self.update_message_box(response, library)
            else:
                return self.update_message_box(response, library) 
        else: 
            return self.update_message_box(authenticate_entries, library)
           
    # Function to search for a book in the library
    def search_book_from_library(self, library):
        book_details = self.view.get_search_book_entry_contents()
        title, author, year, genre = book_details
        authenticate_entries = self.authenticate_entries(title, author, year, genre, "search")
        if "success" in authenticate_entries:
            response = search_book(title, author, year, genre, library)
            if "success" in response[1]:
                books = response[0] 
                self.view.treeview.delete(*self.view.treeview.get_children())
                for book in books:
                    self.view.treeview.insert("", "end", values=book)
                return self.update_message_box(response[1], library)
            else:
                self.handle_threading(self.update_treeview, library)
                return self.update_message_box(response[1], library)
        else:
            self.update_treeview(library)
            return self.update_message_box(authenticate_entries, library)

    # Function to delete a selected book from the library
    def delete_book_from_library(self, library):
        selected_book = self.view.treeview.selection()
        if selected_book:
            responses = []
            for id in selected_book:
                values = self.view.treeview.item(id)["values"]
                title = values[1]
                response = delete_book(title, library)
                responses.append(response)
            self.update_treeview(library)
            for response in responses:
                self.update_message_box(response, library)
            return
        else:
            return self.update_message_box(["Please select a book first", "danger"], library)

    # Function to clear all books from the library
    def clear_all_books_from_library(self, library):
        response = clear_library(library)
        self.update_treeview(library)
        return self.update_message_box(response, library)

    # Function to create or delete a library through a GUI window
    def create_delete_library(self, instruction):
        widgets = self.view.create_new_window(instruction)
        window, label, submit_button, close_button, entry = widgets

        def handle_submission():
            name = entry.get().strip()
            if len(name) > 15:
                return label.config(text="Library name must be less than 15 characters", bootstyle="danger")
            response = create_delete_library_execute(name, "create" if instruction == "Create a new library" else "delete")
            label.config(text=response[0], bootstyle="danger" if response[1] == "danger" else "success")
            global currently_opened_library
            if response[1] == "success" and currently_opened_library == name.capitalize():
                self.handle_threading(self.open_library, "Default_library")
                close_window()
            return self.handle_threading(self.list_libraries)
             
        def close_window():
            window.destroy()
        window.protocol("WM_DELETE_WINDOW", close_window)

        submit_button.config(command=lambda: handle_submission())
        close_button.config(command=lambda: close_window())
    
    # Function to list all libraries in the "libraries" folder
    def list_libraries(self):
        try:
            folder_files = os.listdir("libraries")
            libraries = [file for file in folder_files if file.endswith(".json")]
            self.view.menu_libraries.delete(0, "end")
            for file in libraries:
                if file == "Default_library.json":
                    self.view.menu_libraries.insert_command(0, label=file.strip(".json"), 
                                                command=lambda f=file: self.open_library(f.strip(".json")))
                else:
                    self.view.menu_libraries.add_separator()
                    self.view.menu_libraries.add_command(label=file.strip(".json"), 
                                            command=lambda f=file: self.open_library(f.strip(".json")))
            return
        except PermissionError:
            return print("Permission denied. Unable to access the folder.")
        except Exception as e:
            return print(f"An unexpected error occurred while listing the libraries: {e}")

    # Function to open a library and load its contents
    def open_library(self, library_name):
        global currently_opened_library
        currently_opened_library = library_name
        try:
            with open(f"libraries/{library_name}.json", "r") as file:
                json.load(file)
            self.refresh_library(library_name, "clear_message_box")
            return self.update_message_box([f"{library_name} has been opened.", "success"], library_name)
        except json.JSONDecodeError:
            self.update_message_box([f"Error reading {library_name}.json. Ensure it is valid JSON.", "danger"], library_name)
            self.open_library("Default_library")
            return self.list_libraries()
        except IOError:
            self.update_message_box([f"Error opening {library_name}.json.", "danger"], library_name)
            self.open_library("Default_library")
            return self.list_libraries()
        except FileNotFoundError:
            self.update_message_box([f"{library_name}.json not found.", "danger"], library_name)
            self.open_library("Default_library")
            return self.list_libraries()
        except Exception as e:
            self.update_message_box([f"An unexpected error occurred: {e}", "danger"], library_name)
            self.open_library("Default_library")
            return self.list_libraries()
 
    # Function to handle threading for long-running tasks
    def handle_threading(self, func, *args):
        stop_event.clear()
        thread = threading.Thread(target=func, args=args, daemon=True)
        thread.start()
        self.view.root.update_idletasks()

    # Function to update the treeview with library contents
    def update_treeview(self, library):
        self.view.treeview.delete(*self.view.treeview.get_children())
        books = list_books(library)
        if "success" in books:
            for book in books[0]:
                self.view.treeview.insert("", "end", values=book)
            return
        else:
            return self.update_message_box(books, library)
        
    # Function to refresh the library and clear input fields
    def refresh_library(self, library, with_message_box=False):
        self.view.book_title_entry.delete(0, "end")
        self.view.book_author_entry.delete(0, "end")
        self.view.book_year_entry.delete(0, "end")
        self.view.book_genre_entry.delete(0, "end")

        self.view.search_title_entry.delete(0, "end")
        self.view.search_author_entry.delete(0, "end")
        self.view.search_year_entry.delete(0, "end")
        self.view.search_genre_entry.delete(0, "end")

        self.view.lib_stats_nameval.config(text=currently_opened_library)
        self.view.lib_stats_numbooksval.config(text=f"{get_num_books(library)}")

        if with_message_box:
            self.clear_message_box(library)
        return self.update_treeview(library)
        
    # Function to clear the message box
    def clear_message_box(self, library):
        return self.handle_threading(self.update_message_box, [f"{library} has been opened.", "success"], library)

    # Function to sort the library based on a key
    def sort_library(self, library):
        key = self.view.sort_book_entry.get()
        if key.strip() != "":
            respond = sort_books(key, library)
            if "success" in respond:
                self.update_treeview(library)
                return self.update_message_box(respond, library)
            else:
                return self.update_message_box(respond, library)
        else:
            return self.update_message_box(["Please selected a key for books sorting", "danger"], library)

    # Function to create one million book entries
    def create_million_books(self, library):
        widgets = self.view.create_million_book_window()
        window, progress_bar, label, start_button, close_button = widgets

        # Function to create books
        def create():
            try:
                response = create_mill_books(stop_event, progress_bar, window, label, self.view.treeview, library)
                label.config(text=f"{response if len(response) <= 80 else response[:80]+"..."}", bootstyle="success")
            except Exception as e:
                label.config(text=f"Error: {e}", bootstyle="danger")

        # Function to stop the creation process
        def stop_creating():
            stop_event.set()  # Signal the thread to stop
        
        def close_window():
            stop_event.set()  # Signal the thread to stop
            window.destroy()
        window.protocol("WM_DELETE_WINDOW", close_window)

        start_button.config(command=lambda: self.handle_threading(create))
        close_button.config(command=lambda: stop_creating())

    # Function to search for a book using text extracted from an image
    def search_book_with_image(self, library):
        widgets = self.view.search_with_image()
        if not widgets:
            self.update_message_box(["Error: Unable to load the search with image widgets.", "danger"], library)
            return
        window, label, button = widgets
       
        def search_text(): 
            text_from_image = self.view.text_in_image
            if not text_from_image:
                self.update_message_box(["No valid text found in the image.", "danger"], library)
                return
            title = author = year = genre = text_from_image
            # print(text_from_image)
            response = search_book(title, author, year, genre, library, text_from_image)
            if "success" in response[1]:
                books = response[0]
                self.view.treeview.delete(*self.view.treeview.get_children())
                for book in books:
                    self.view.treeview.insert("", "end", values=book)
                self.update_message_box(response[1], library)
            else:
                self.update_message_box(response[1], library)
        def close_window():
            window.destroy()
        window.protocol("WM_DELETE_WINDOW", close_window)

        button.config(command=lambda: search_text())
