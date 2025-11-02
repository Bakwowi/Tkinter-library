from tkinter import *
from tkinter import messagebox, filedialog
import tkinter.font as tk_font
import os

try:
    import ttkbootstrap as tb
    from tkinter import ttk
    from ttkbootstrap.constants import *
except ImportError:
    messagebox.showerror("Module Error", "The 'ttkbootstrap' module is not installed. Please install it using 'pip install ttkbootstrap'")
    exit()

try:
    from PIL import Image, ImageTk
except ImportError:
    messagebox.showerror("Module Error", "The 'Pillow' module is not installed. Please install it using 'pip install Pillow'")
    exit()

try:
    import pyocr
    import pyocr.builders
except ImportError:
    messagebox.showerror("Module Error", "The 'pyocr' module is not installed. Please install it using 'pip install pyocr'")
    exit()

class ViewClass:
    def __init__(self, root):
        # Attempt to add the default Tesseract installation path to the environment
        # This helps pyocr find Tesseract if it wasn't added to PATH during installation.
        tesseract_path = r"C:\\Program Files\\Tesseract-OCR"
        if tesseract_path not in os.environ['PATH']:
            os.environ['PATH'] += os.pathsep + tesseract_path

        self.tools = pyocr.get_available_tools()
        if not self.tools:
            messagebox.showerror("OCR Engine Not Found", "Tesseract OCR was not found.\nPlease ensure it is installed and that its location is in your system's PATH.")
            root.destroy()
            return
        self.tool = self.tools[0]


        self.root = root

        self.root.title("Library Management System")
        self.root.resizable(False, False)

        width = 1380
        height = 810
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        print(screen_width, screen_height)
        self.x_position = int((screen_width / 2) - (width / 2))
        self.y_position = int((screen_height / 2) - ((height + 100) / 2))
        self.root.geometry(f"{width}x{height}+{self.x_position}+{self.y_position}")

        # Configure the grid weights for the root window
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        
        # Configure the menu bar
        self.root.option_add('*tearOff', FALSE)
        self.menu = tb.Menu(self.root)
        self.root['menu'] = self.menu

        # Add "File" and "Libraries" menus
        self.menu_file = Menu(self.menu)
        self.menu_libraries = Menu(self.menu)
        self.menu_themes = Menu(self.menu)
        self.menu.add_cascade(menu=self.menu_file, label='File')
        self.menu.add_cascade(menu=self.menu_libraries, label='Libraries')
        self.menu.add_cascade(menu=self.menu_themes, label="Themes")

        # Add commands to the "File" menu
        self.menu_file.add_command(label="Create a new library")
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Delete a library")
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Create one million books")
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=lambda: self.on_closing())

        def change_library_theme(self_root, theme):
            self_root.style = tb.Style(theme)
            self_root.root.style.theme_use(theme)

        themes = [
            ("flatly", "Clean, flat, modern UI"),
            ("journal", "Paper-like appearance"),
            ("lumen", "Bright, high-contrast"),
            ("minty", "Fresh green accents"),
            ("pulse", "Vivid purple-blue tones"),
            ("sandstone", "Warm, beige look"),
            ("united", "Classic red theme"),
            ("yeti", "Clean white interface"),
            ("cosmo", "Rounded and modern look"),
            ("morph", "Gentle, soft flat UI"),
            ("simplex", "Simple, uncluttered design"),
            ("darkly", "Dark theme with teal accents"),
            ("cyborg", "Very dark with neon blue"),
            ("superhero", "Comic-book inspired dark look"),
            ("solar", "Warm yellow/orange tones"),
            ("vapor", "Neon/pastel dark retro look")
        ]
        for theme, description in themes:
            self.menu_themes.add_command(label=f"{theme}", command=lambda theme_name=theme: change_library_theme(self, theme_name))
            self.menu_themes.entryconfig(f"{theme}", accelerator=f"{description}")

        # Left frame
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.grid(column=0, row=0, padx=(10, 0), pady=20, sticky="news")
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(3, weight=1)

        self.add_label_frame = ttk.Labelframe(self.left_frame, text="Add a book", bootstyle="info")
        self.add_label_frame.grid(sticky="news")
        self.add_label_frame.columnconfigure(1, weight=1)

        self.book_label1 = ttk.Label(self.add_label_frame, text="Title:")
        self.book_label1.grid(column=0, row=0, padx=10, pady=10, sticky="w")
        self.book_title_entry = ttk.Entry(self.add_label_frame, width=30)
        self.book_title_entry.grid(column=1, row=0, padx=10, pady=10, sticky="e")
        self.book_title_entry.focus()

        self.book_label2 = ttk.Label(self.add_label_frame, text="Author:")
        self.book_label2.grid(column=0, row=1, padx=10, pady=10, sticky="w")
        self.book_author_entry = ttk.Entry(self.add_label_frame, width=30)
        self.book_author_entry.grid(column=1, row=1, padx=10, pady=10, sticky="e")

        self.book_label3 = ttk.Label(self.add_label_frame, text="Year:")
        self.book_label3.grid(column=0, row=2, padx=10, pady=10, sticky="w")
        self.book_year_entry = ttk.Entry(self.add_label_frame, width=30)
        self.book_year_entry.grid(column=1, row=2, padx=10, pady=10, sticky="e")

        self.book_label5 = ttk.Label(self.add_label_frame, text="Genre:")
        self.book_label5.grid(column=0, row=3, padx=10, pady=10, sticky="w")
        self.book_genre_entry = ttk.Combobox(self.add_label_frame,
                                             width=28, values=("Fantasy", "Science Fiction",
                                                               "Action & Adventure", "Science & Technology",
                                                               "Mystery", "Horror","Dystopian", "Thriller & Suspense", "Classic",
                                                               "Romance", "Food & Drink", "Art & Photography",
                                                               "History", "Travel", "Humor", "Guide/How-to",
                                                               "Religion & Spirituality", "Historical Fiction", 
                                                               "Humanities & Social Sciences"))

        self.book_genre_entry.grid(column=1, row=3, padx=10, pady=10, sticky="e")

        self.add_book_button = ttk.Button(self.add_label_frame, text="➕ Add Book", bootstyle="success", cursor="hand2")
        self.add_book_button.grid(column=0, row=4, columnspan=2, padx=20, pady=15)

        self.library_stats_frame = ttk.Labelframe(self.left_frame, text="Library statistics", bootstyle="info")
        self.library_stats_frame.grid(column=0, row=1, sticky="nwes", pady=(10, 0))
        self.library_stats_frame.columnconfigure(1, weight=1)

        self.lib_stats_name = ttk.Label(self.library_stats_frame, text="Library: ")
        self.lib_stats_name.grid(column=0, row=0, padx=10, pady=10, sticky="w")
        self.lib_stats_nameval = ttk.Label(self.library_stats_frame, text="Default library")
        self.lib_stats_nameval.grid(column=1, row=0, sticky="w")

        self.lib_stats_numbooks = ttk.Label(self.library_stats_frame, text="Number of books: ")
        self.lib_stats_numbooks.grid(column=0, row=1, padx=10, pady=10, sticky="w")
        self.lib_stats_numbooksval = ttk.Label(self.library_stats_frame, text="100")
        self.lib_stats_numbooksval.grid(column=1, row=1, padx=10, pady=10)

        self.lib_stats_num_books_av = ttk.Label(self.library_stats_frame, text="Number of books available: ")
        self.lib_stats_num_books_av.grid(column=0, row=2, padx=10, pady=10, sticky="w")
        self.lib_stats_num_books_av_val = ttk.Label(self.library_stats_frame, text="✖")
        self.lib_stats_num_books_av_val.grid(column=1, row=2, padx=10, pady=10)

        self.lib_stats_numbooks_del = ttk.Label(self.library_stats_frame, text="Number of books deleted: ")
        self.lib_stats_numbooks_del.grid(column=0, row=3, padx=10, pady=10, sticky="w")
        self.lib_stats_numbooks_del_val = ttk.Label(self.library_stats_frame, text="✖")
        self.lib_stats_numbooks_del_val.grid(column=1, row=3, padx=10, pady=10)

        self.message_box = ttk.Labelframe(self.left_frame, text="Message box", bootstyle="success")
        self.message_box.grid(column=0, row=2, pady=(10, 0), sticky="nwes")
        self.message_label = ttk.Label(self.message_box, text="Default library opened", bootstyle="success", wraplength=250)
        self.message_label.grid(column=0, row=0, padx=10, pady=10, sticky="nwes")

        font_name = "Brush Script MT" if "Brush Script MT" in tk_font.families() else "italic"
        self.signature = ttk.Label(self.left_frame, text="By Bakwowi Junior", font=(font_name, 20))
        self.signature.place(relx=0.0, rely=0.97, anchor="w")

        # Right frame
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.grid(column=1, row=0, padx=(10, 10), pady=20, sticky="nwes")
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.rowconfigure(1, weight=1)

        self.right_top_frame = ttk.Frame(self.right_frame)
        self.right_top_frame.grid(column=0, row=0, sticky="nwes")

        # Search label frame
        self.search_label_frame = ttk.Labelframe(self.right_top_frame, text="Search for a book", bootstyle="info")
        self.search_label_frame.grid(column=0, row=0, sticky="nwes")
        self.search_label_frame.columnconfigure(3, weight=1)

        self.search_title = ttk.Label(self.search_label_frame, text="Title:", anchor="w", justify="left")
        self.search_title.grid(column=0, row=0, padx=10, pady=(10, 0), sticky="w")
        self.search_title_entry = ttk.Entry(self.search_label_frame, width=20)
        self.search_title_entry.grid(column=0, row=1, padx=10, pady=10)

        self.search_author = ttk.Label(self.search_label_frame, text="Author:", anchor="w", justify="left")
        self.search_author.grid(column=1, row=0, padx=10, pady=(10, 0), sticky="w")
        self.search_author_entry = ttk.Entry(self.search_label_frame, width=20)
        self.search_author_entry.grid(column=1, row=1, padx=10, pady=10)

        self.search_year = ttk.Label(self.search_label_frame, text="Year:", anchor="w", justify="left")
        self.search_year.grid(column=2, row=0, padx=10, pady=(10, 0), sticky="w")
        self.search_year_entry = ttk.Entry(self.search_label_frame, width=20)
        self.search_year_entry.grid(column=2, row=1, padx=10, pady=10)

        self.search_genre = ttk.Label(self.search_label_frame, text="Genre:", anchor="w", justify="left")
        self.search_genre.grid(column=3, row=0, padx=10, pady=(10, 0), sticky="w")
        self.search_genre_entry = ttk.Combobox(self.search_label_frame, width=20, values=("Fantasy", "Science Fiction",
                                                                                         "Action & Adventure", "Science & Technology",
                                                                                         "Mystery", "Horror", "Thriller & Suspense",
                                                                                         "Romance", "Food & Drink", "Art & Photography",
                                                                                         "History", "Travel", "Humor", "Guide/How-to",
                                                                                         "Religion & Spirituality", "Historical Fiction",
                                                                                           "Humanities & Social Sciences"))
        self.search_genre_entry.grid(column=3, row=1, padx=10, pady=10, sticky="w")

        self.search_button = ttk.Button(self.search_label_frame, text="🔍 Search", bootstyle="success", cursor="hand2")
        self.search_button.grid(column=3, row=4, padx=10, pady=10, sticky="w")

        self.search_image_label = ttk.Label(self.search_label_frame, text="Or")
        self.search_image_label.grid(column=0, row=3, columnspan=3)
        self.search_image_button = ttk.Button(self.search_label_frame, text="Click here to search from an image", 
                                              bootstyle="success-outline", cursor="hand2")
        self.search_image_button.grid(column=0, row=4, columnspan=3, padx=10, pady=10, sticky="we")

        self.refresh_button = ttk.Button(self.right_top_frame, text="Refresh\nLibrary", bootstyle="info-outline", width=21, cursor="hand2")
        self.refresh_button.grid(column=1, row=0, padx=(10, 0), pady=(8, 0), sticky="nes")


        self.right_middle_frame = ttk.Frame(self.right_frame)
        self.right_middle_frame.grid(column=0, row=1, pady=(10, 0), sticky="news")
        self.right_middle_frame.columnconfigure(1, weight=1)

        # Books Listing using a treeview frame
        columns = ("ID", "Title", "Author", "Year", "Genre", "Status")
        self.treeview = ttk.Treeview(self.right_middle_frame, columns=columns, show="headings", height=24, bootstyle="secondary", cursor="hand2")
        self.treeview.grid(column=0, row=0, columnspan=2, sticky="news")
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor="center", width=129)
        self.scrollbar = ttk.Scrollbar(self.right_middle_frame, orient="vertical", bootstyle="info-round", command=self.treeview.yview, cursor="hand2")
        self.scrollbar.grid(column=1, row=0, sticky="nse")
        self.treeview.config(yscrollcommand=self.scrollbar.set)
        
        self.last_item = None
        def hover_effect(event):
            region = self.treeview.identify("region", event.x, event.y)
            if region == "cell":
                current_item = self.treeview.identify_row(event.y)
                if current_item != self.last_item:
                    if self.last_item:
                        self.treeview.item(self.last_item, tags=())
                    self.treeview.item(current_item, tags=("hover",))
                    self.last_item = current_item
            else:
                if self.last_item:
                    self.treeview.item(self.last_item, tags=())
                    self.last_item = None
        def clear_hover_effect(event):
            if self.last_item:
                self.treeview.item(self.last_item, tags=())
                self.last_item = None
        self.treeview.tag_configure("hover", background="#9A9A9A")

        self.right_bottom_frame = ttk.Frame(self.right_frame)
        self.right_bottom_frame.grid(column=0, row=3, pady=(10, 0), sticky="news")
        # self.right_bottom_frame.columnconfigure(0, weight=0)
        self.right_bottom_frame.columnconfigure(1, weight=1)    

        self.sort_book_entry = ttk.Combobox(self.right_bottom_frame, values=("title", "author", "year"))
        self.sort_book_entry.grid(column=0, row=0,  sticky="ws")
        self.sort_book_button = ttk.Button(self.right_bottom_frame, text="⬆ Sort", bootstyle="info", cursor="hand2")
        self.sort_book_button.grid(column=0, row=0, padx=(200, 0), sticky="ws")


        self.clear_all_books_button = ttk.Button(self.right_bottom_frame, text="🧹 Clear all books", bootstyle="danger-outline", cursor="hand2")
        self.clear_all_books_button.grid(column=1, row=0, padx=(0, 100), sticky="e")

        self.delete_book_button = ttk.Button(self.right_bottom_frame, text="✖ Delete", bootstyle="danger", cursor="hand2")
        self.delete_book_button.grid(column=1, row=0, padx=(10, 0), sticky="e")

        self.treeview.bind("<Motion>", hover_effect)
        self.treeview.bind("<Leave>", clear_hover_effect)
        

        # self.root.mainloop()

    def get_add_book_entry_contents(self):
        book_title = self.book_title_entry.get()
        book_author = self.book_author_entry.get()
        book_year = self.book_year_entry.get()
        book_genre = self.book_genre_entry.get()

        return [book_title, book_author, book_year, book_genre]
    
    def get_search_book_entry_contents(self):
        book_title = self.search_title_entry.get()
        book_author = self.search_author_entry.get()
        book_year = self.search_year_entry.get()
        book_genre = self.search_genre_entry.get()
        return [book_title, book_author, book_year, book_genre]
    
    def show_message(self, message, library):
        self.message_box.config(bootstyle=f"{message[1]}")
        self.message_label.config(text=f"{library}:\n{message[0]}", bootstyle=f"{message[1]}")

    def create_new_window(self, instruction):
        new_window = Toplevel(self.root)
        new_window.title("Create a new library" if instruction == "Create a new library" else "Delete a library")
        new_window.resizable(False, False)

        # Center the new window over the main window
        win_width = 380
        win_height = 200

        parent_x = self.root.winfo_x()
        parent_y = self.root.winfo_y()
        parent_width = self.root.winfo_width()
        parent_height = self.root.winfo_height()

        x = parent_x + (parent_width // 2) - (win_width // 2)
        y = parent_y + (parent_height // 2) - (win_height // 2)
        new_window.geometry(f"{win_width}x{win_height}+{x}+{y}")

        #Set the label text based on the action
        label_text = ("Enter the name of the library you want to create" 
                    if instruction == "Create a new library" 
                    else "Enter the name of the library you want to delete")
        
        label1 = ttk.Label(new_window, text=label_text, bootstyle="info")
        label1.grid(padx=20, pady=20, column=0, row=0, columnspan=2)

        entry = ttk.Entry(new_window, width=40)
        entry.grid(column=0, row=1, columnspan=2, padx=20)
        entry.focus()

        label2 = ttk.Label(new_window, text="", bootstyle="success", wraplength=220)
        label2.place(x=50, y=115, anchor="w")
        
        button_submit = ttk.Button(new_window, 
                                text='Create' if instruction == 'Create a new library' else 'Delete', 
                                bootstyle="success-outline", cursor="hand2")
        button_submit.grid(column=0, row=3, padx=(30, 0), pady=60)

        #Close the window and re-enable the command entry
        
        button_close = ttk.Button(new_window, text="Close", bootstyle="danger", cursor="hand2")
        button_close.grid(column=1, row=3, padx=(0, 30), pady=60)

        return [new_window, label2, button_submit, button_close, entry]

    def create_million_book_window(self):
        new_window = Toplevel(self.root)
        new_window.resizable(False, False)
        new_window.geometry("300x180+530+280")
        new_window.title("Create one million book entries")
        new_window.focus()
        

        label1 = ttk.Label(new_window, text="Click 'Create' to create 1 million books", bootstyle="info")
        label1.grid(column=0, row=0, columnspan=2, padx=40, pady=15)

        progress_bar = ttk.Progressbar(new_window, orient="horizontal",
                                       length=200, mode="determinate", bootstyle="success")
        progress_bar.grid(column=0, row=1, columnspan=2)

        label2 = ttk.Label(new_window, text="", wraplength=200)
        label2.grid(column=0, row=3, columnspan=2, padx=30, pady=10)

        create_button = ttk.Button(new_window, text="Create", bootstyle="success", cursor="hand2")
        create_button.grid(column=0, row=4, padx=(30, 0), pady=10)

        cancel_button = ttk.Button(new_window, text="Cancel", bootstyle="danger", cursor="hand2")
        cancel_button.grid(column=1, row=4, padx=(0, 30), pady=10)

        return [new_window, progress_bar, label2, create_button, cancel_button]

    def search_with_image(self):
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.rect_id = None
        self.text_in_image = None
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if not file_path:
            return  # Exit if no file is selected

        image = Image.open(file_path)

        canvas_width = 400
        canvas_height = 340
        image_ratio = image.width / image.height
        canvas_ratio = canvas_width / canvas_height

        if image_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / image_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * image_ratio)

        resized_image = image.resize((new_width, new_height))
        tk_image = ImageTk.PhotoImage(resized_image)

        
        new_window = Toplevel(self.root)
        new_window.resizable(False, False)
        new_window.geometry("450x500+480+100")
        new_window.title("Search book from image")

        new_window.columnconfigure(0, weight=1)
        new_window.rowconfigure(0, weight=1)
        

        
        frame = ttk.Frame(new_window, borderwidth=4, relief="solid")
        frame.grid( sticky="nwes")
        # frame.columnconfigure(0, weight=1)
        # frame.rowconfigure(0, weight=1)

        canvas = Canvas(frame, width=canvas_width, height=canvas_height, borderwidth=2, relief="solid", background="white")
        canvas.grid(column=0, row=0, padx=20, pady=20, sticky="nwe")

        x_offset = (canvas_width - new_width) // 2
        y_offset = (canvas_height - new_height) // 2

        canvas.create_image(x_offset, y_offset, anchor="nw", image=tk_image)

        label = ttk.Label(frame, text="Search query: max -> 180 characters", wraplength=400, bootstyle="info")
        label.grid(column=0, row=1, padx=20, pady=(0, 10), sticky="we")

        search_button = ttk.Button(frame, text="Search", bootstyle="success", cursor="hand2")
        search_button.grid(column=0, row=2, padx=20, sticky="we")

        #Store a reference to the image to prevent garbage collection
        canvas.image_reference = tk_image

        def on_button_press(event):
            if self.rect_id:
                canvas.delete(self.rect_id)
            
            self.start_x = event.x
            self.start_y = event.y

            self.rect = canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)
            self.rect_id = self.rect
            # print(self.rect)
        
        def on_mouse_drag(event):
            if self.start_x != event.x and self.start_y != event.y:
                canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

        def on_button_release(event):
            canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
            if self.start_x != event.x and self.start_y != event.y:
                identify_text_in_rect(self.start_x, self.start_y, event.x, event.y)

        def identify_text_in_rect(x1, y1, x2, y2):
            # Adjust coordinates for padding
            left = min(x1, x2) - x_offset
            right = max(x1, x2) - x_offset
            top = min(y1, y2) - y_offset
            bottom = max(y1, y2) - y_offset

            # Clamp values to image dimensions
            left = max(left, 0)
            top = max(top, 0)
            right = min(right, new_width)
            bottom = min(bottom, new_height)

            cropped_image = resized_image.crop((left, top, right, bottom))

            
            #Extract text from the cropped image
            self.text_in_image = self.tool.image_to_string(cropped_image, lang="eng", builder=pyocr.builders.TextBuilder())

            #Normalize the text: remove newlines and extra spaces
            self.text_in_image = " ".join(self.text_in_image.split())
            
            #Update the label with the cleaned text
            label.config(text=f"Search query: {self.text_in_image if len(self.text_in_image) <= 180 else self.text_in_image[:50] + '...'}")

        

        canvas.bind("<ButtonPress-1>", on_button_press)
        canvas.bind("<B1-Motion>", on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", on_button_release)

        return [new_window, label, search_button]
        
    def on_closing(self):
        if messagebox.askquestion("Quit MyLibrary app", "Do you want to quit?", icon="info") == 'yes':
            self.root.destroy()
