import json
import datetime
import os
import random
import threading 

#Event to handle stopping of the creation of a million books
stop_event = threading.Event()


#This function retrieves the library data from a JSON file
def get_library(library_name="Default_library"):
    try:
        #Attempt to open and load the library file
        with open("libraries/" + library_name + ".json", "r") as file:
            library = json.load(file)
        return library
    except FileNotFoundError:
        #Return error if the library file does not exist
        return ["Library file not found.", "danger"]
    except Exception as e:
        #Handle unexpected errors and create an empty library file
        with open("libraries/" + library_name + ".json", "w") as file:
            json.dump([], file, indent=4)
        return [f"An unexpected error occurred: {e}\n Please try again", "danger"]

#This function updates the library with new data
def update_library(new_book, library_name="Default_library"):
    try:
        #Write the updated library data to the file
        with open("libraries/" + library_name + ".json", "w") as file:
            json.dump(new_book, file, indent=4)
        return ["Library updated successfully", "success"]
    except IOError:
        #Handle errors during file writing
        return ["An error occurred while updating the library.\n Please try again", "danger"]

#This function retrieves the total number of books in the library
def get_num_books(library_name="Default_library"):
    #Count the number of books in the library
    num_books = len(get_library(library_name))
    return num_books

#This function adds a new book to the library
def add_book(title, author, year, genre, library_name="Default_library"):
    try:
        #Create a new book dictionary with details
        new_book = {}
        date = datetime.datetime.now()
        new_book["title"] = title
        new_book["author"] = author
        #Validate the year input
        try:
            new_book["year"] = int(year)
        except ValueError:
            return ["Invalid year. Please enter a valid number for the year.", "danger"]
        
        new_book["genre"] = genre
        new_book["status"] = "available"
        new_book["date_added"] = date.strftime("%B-%d-%Y %H:%M:%S")
        library = get_library(library_name)

        #Check for errors in retrieving the library
        if "error" in library:
            return library

        #Check if the book already exists in the library
        for book in library:
            if new_book["title"].lower() == book["title"].lower():
                return ["This book already exists.", "danger"]

        #Add the new book to the library and update it
        library.append(new_book)
        update_library(library, library_name)
        return ["Book added successfully.", "success"]

    except Exception as e:
        #Handle unexpected errors during book addition
        return [f"An unexpected error occurred while adding the book: {e}\nPlease try again", "danger"]

#This function deletes a book from the library by its title
def delete_book(title, library_name="Default_library"):
    try:
        book_title = title
        library = get_library(library_name)

        #Check if the library is empty
        if not library:
            return ["The library is empty. Nothing to delete.", "danger"]

        #Search for the book and remove it if found
        for book in library:
            if book["title"].lower() == book_title.lower():
                library.remove(book)
                update_library(library, library_name)
                return ["Book(s) deleted successfully.", "success"]

        #Return error if the book is not found
        return ["Book not found", "danger"]
    except Exception as e:
        #Handle unexpected errors during book deletion
        return [f"An unexpected error occurred while deleting the book: {e}\nPlease try again", "danger"]

#This function searches for a book in the library based on its title, author, and year
def search_book(title="", author="", year="", genre="", library_name="Default_library"):
    try:
        library = get_library(library_name)
        if "danger" in library:
            return library
        if not library:
            return ["The library is empty. No books to search from.", "danger"]

        books_found = []

        # Normalize image text
        # text_image = text_from_image.lower().strip() if text_from_image != None else ""
        # use_text = bool(text_image)
        # print(title, author, year, genre)
        for index, book in enumerate(library, start=1):
            # Use text from image
            # print(text_image)
            # if use_text:
            #     matches_title = (book["title"].lower() in title.lower() or title.lower() in book["title"]) if title else True
            #     matches_author = (book["author"].lower() in author.lower() or author.lower() in book["author"]) if author else True
            #     matches_genre = (book["genre"].lower() in genre.lower() or genre.lower() in book["genre"]) if genre else True
            #     matches_year = year in str(book["title"]) if year else True
            #     print(text_image, matches_title, matches_author, matches_year, matches_genre)
            # if not use_text:
            # print(title, book["title"])

            matches_title = (title.lower() in book["title"].lower() or book["title"] in title.lower()) if title else True
            matches_author = (author.lower() in book["author"].lower() or book["author"] in author.lower()) if author else True
            matches_genre = (genre.lower() in book["genre"].lower() or book["genre"] in genre.lower()) if genre else True
            matches_year = (year in str(book["year"])) if year else True



            if matches_title and matches_author and matches_year and matches_genre:
                books_found.append((
                    index,
                    book.get('title', 'unknown'),
                    book.get('author', 'unknown'),
                    book.get('year', 'unknown'),
                    book.get('genre', 'unknown'),
                    book.get('status', 'unknown')
                ))

        return [books_found, ["Book(s) successfully found", "success"]] if books_found else [[], ["Book not found", "danger"]]

    except ValueError:
        return ["Invalid year. Please enter a valid number for the year.", "danger"]
    except Exception as e:
        return [f"An error occurred while searching for the book: {e}\nPlease try again", "danger"]

#This function lists all books in the library with their details
def list_books(library_name="Default_library"):
    try:
        library = get_library(library_name)
        
        #Check if the library is empty
        if not library:
            return ["The library is empty. No books to list.", "danger"]

        #Format the list of books
        books_list = []
        for i, book in enumerate(library, start=1):
            books_list.append((i, book.get('title', 'unknown'), book.get('author', 'unknown'), 
                              book.get('year', 'unknown'), book.get('genre', 'unknown'), 
                              book.get('status', 'unknown')))
        return [books_list, "success"]
    except Exception as e:
        #Handle unexpected errors during book listing
        return [f"An error occurred while listing the books: {e}\nPlease try again", "danger"]

#This function sorts the books in the library by their title
def sort_books(key, library_name="Default_library"):
    library = get_library(library_name)
    if not library:
        return ["The library is empty. No books to sort.", "danger"]
    
    try:
        #Sort the books alphabetically by title
        if key not in ["title", "author", "year", "genre"]:
            return ["Invalid sorting key. Please use 'title', 'author', 'year', or 'genre'.", "danger"]
        sorted_books = sorted(library, key=lambda book: book[key])
        #Update the library with the sorted list
        update_library(sorted_books, library_name)
        return ["All the books have been successfully sorted", "success"]
    except Exception as e:
        #Handle errors during sorting
        return [f"An error occurred while trying to sort the books: {e}\nPlease try again", "danger"]

#This function clears all books in the library by overwriting it with an empty list
def clear_library(library_name="Default_library"):
    try:
        with open(f"libraries/" + library_name + ".json", "w") as file:
            json.dump([], file, indent=4)
        return ["The library has been successfully cleared.", "success"]
    except IOError:
        #Handle errors during file clearing
        return ["An error occurred while clearing the library.", "danger"]

#This function creates or deletes a library based on the instruction
def create_delete_library_execute(library_name, instruction): 
    if library_name.strip() == "":
        return ["Please enter a proper library name", "danger"]
    
    if instruction == "create":
        #Check if the library already exists
        if os.path.exists(f"libraries/{library_name}.json"):
            return ["The library you want to create already exists", "danger"]
    
        try:
            #Create a new library file
            with open(f"libraries/{library_name.capitalize()}.json", "w") as file:
                json.dump([], file, indent=4)
            return [f"{library_name} has been successfully created", "success"]
        except IOError:
            #Handle I/O errors during library creation
            return ["An I/O error occurred while creating your library", "danger"]
        except Exception as e:
            #Handle unexpected errors during library creation
            return [f"An unexpected error occurred: {e}\nPlease try again", "danger"]

    elif instruction == "delete":
        #Check if the library exists
        if not os.path.exists(f"libraries/{library_name.capitalize()}.json"):
            return ["Library not found.", "error"]
        if library_name == "default_library":
            return ["You cannot delete the default library.", "danger"]
        try:
            #Delete the library file
            os.remove(f"libraries/{library_name}.json")
            return [f"{library_name} has been successfully deleted", "success"]
        except FileNotFoundError:
            #Handle missing file errors
            return ["The library you want to delete is missing", "danger"]
        except PermissionError:
            #Handle permission errors
            return ["Permission denied. Unable to delete the library.", "danger"]
        except IOError:
            #Handle I/O errors during library deletion
            return ["An I/O error occurred while deleting your library", "danger"]
        except Exception as e:
            #Handle unexpected errors during library deletion
            return [f"An unexpected error occurred: {e}\nPlease try again", "danger"]

#This function generates a large number of random books and adds them to the library
def create_mill_books(stop_event_thread, progress_bar, new_window, label, treeview, library_name="Default_library"):
    num_books = 1000  #Number of books to generate

    rand_titles = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    rand_authors = [
    "Alex Michaelides",
    "Tara Westover",
    "Delia Owens",
    "Matt Haig",
    "Andy Weir",
    "Madeline Miller",
    "Madeline Miller",
    "Erin Morgenstern",
    "Taylor Jenkins Reid",
    "Miranda Cowley Heller",
    "Taylor Jenkins Reid",
    "Taylor Jenkins Reid",
    "Bonnie Garmus",
    "Gabrielle Zevin",
    "TJ Klune",
    "Shelby Van Pelt",
    "Colleen Hoover",
    "Janet Skeslien Charles",
    "Sarah J. Maas",
    "Rebecca Yarros"
]
    rand_years = [
    "2019",
    "2018",
    "2016",
    "2025",
    "2007",
    "2002",
    "2011",
    "2014",
    "2017",
    "1983",
    "1976",
    "1999",
    "1994",
    "1912",
    "2020",
    "2022",
    "1988",
    "2021",
    "2015",
    "2023"
]
    rand_genres = [
    "Thriller & Suspense",
    "History",
    "Mystery",
    "Guide/How-to",
    "Science Fiction",
    "Historical Fiction",
    "History",
    "Religion & Spirituality",
    "Art & Photography",
    "Fiction",
    "Historical Fiction",
    "Fiction",
    "Historical Fiction",
    "Action & Adventure",
    "Fantasy",
    "Food & Drink",
    "Thriller & Suspense",
    "Humanities & Social Sciences",
    "Horror",
    "Romance"
]

    progress_bar["value"] = 0  #Initialize progress bar

    label.config(text="Creating .......", bootstyle="success")
    for i in range(num_books):  #Generate books in a loop
        count = 0
        if stop_event_thread.is_set():  #Check if the stop_event is set
            return "Book creation was cancelled."  #Exit if stop_event is set
        try:
            if count <= num_books:
                #Generate random book details
                title = "".join(random.choices(rand_titles, k=random.randint(2, 15)))  #Random title
                author = rand_authors[random.randint(0, 19)]  #Random author
                year = rand_years[random.randint(0, 19)]  #Random 4-digit year
                genre = rand_genres[random.randint(0, 19)]  #Random genre

                result = add_book(title, author, year, genre, library_name)  #Add book to library
                progress = (i / num_books) * 200  #Update progress
                progress_bar["value"] = progress
                new_window.update_idletasks()
                if "success" in result:
                    treeview.insert("", "end", values=(i+1, title, author, year, genre, "Available"))

                if "danger" in result:
                    return f"Error adding book: {result[0]}"
            else:
                return "Books creation has ended"
        except Exception as e:
            #Handle unexpected errors during book creation
            return f"An unexpected error occurred while creating books:\n{e}"
    return f"{num_books} books successfully created"
