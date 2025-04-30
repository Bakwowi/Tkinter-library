# 📚 Tkinter Library

This project features a library management system with a graphical interface built using **Tkinter**, styled with **ttkbootstrap**, and includes functionality to extract text from images using **OCR (Optical Character Recognition)**.

---

## 🖼 GUI with Tkinter & ttkbootstrap

The user interface is created using the built-in Python GUI library **Tkinter**, enhanced with **ttkbootstrap** for a modern and theme-rich look.

### Why `ttkbootstrap`?
- Provides modern themes and styling for default Tkinter widgets.
- Offers a wide variety of built-in themes to choose from.
- Enhances usability and visual appeal.

### 🔧 Installation
To install `ttkbootstrap`, run:
```bash
pip install ttkbootstrap
```

## 🖼️ Extracting Text from Images (OCR)
To extract text from images, the project uses OCR via the pyocr Python library and Tesseract OCR engine.

### Required Tools:
- pyocr: Python wrapper for OCR engines.
- Pillow: For handling images.
- Tesseract OCR: The OCR engine.

## 🔧 Installation
Install the Python dependencies:

```bash
pip install pyocr pillow
```

Then install Tesseract OCR by following the official instructions: 👉 https://tesseract-ocr.github.io/tessdoc/Installation.html


## 🛠 Project Structure
```bash
tkinter-library/
├── tests/
│   ├── model_unit_test.py              # Unit tests for the model
│   ├── controller_integration_test.py  # Integration tests for the controller
│   └── system_test.py                  # System-level testing
├── main.py                             # Entry point for the application
├── view.py                             # UI logic and rendering
├── controller.py                       # Handles logic between view and model
├── model.py                            # Business logic and data handling
└── README.md                           # Project documentation              
```

## ✅ Prerequisites
- Python 3.7+
- pip (Python package installer)
- Internet access (for installing libraries and OCR engine)

## 🙏 Authors & Acknowledgments
# Project Author
- Bakwowi Junior

# Acknowledgments
- Thanks to all contributors and libraries used in this project:
- Python community
- Open-source libraries: Tkinter, ttkbootstrap, Pillow, pyocr
- Tesseract OCR developers