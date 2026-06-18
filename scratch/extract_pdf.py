import sys
import os

def extract_pdf_text(pdf_path, txt_path):
    # Try using fitz (PyMuPDF)
    try:
        import fitz
        doc = fitz.open(pdf_path)
        text = ""
        for i, page in enumerate(doc):
            text += f"=== PAGE {i+1} ===\n"
            text += page.get_text() + "\n"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Extracted using fitz successfully!")
        return
    except ImportError:
        pass

    # Try using pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for i, page in enumerate(pdf.pages):
                text += f"=== PAGE {i+1} ===\n"
                text += (page.extract_text() or "") + "\n"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Extracted using pdfplumber successfully!")
        return
    except ImportError:
        pass

    # Try using pypdf
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages):
            text += f"=== PAGE {i+1} ===\n"
            text += (page.extract_text() or "") + "\n"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Extracted using pypdf successfully!")
        return
    except ImportError:
        pass

    # Try using PyPDF2
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages):
            text += f"=== PAGE {i+1} ===\n"
            text += (page.extract_text() or "") + "\n"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Extracted using PyPDF2 successfully!")
        return
    except ImportError:
        pass

    print("Error: No PDF extraction library found (fitz, pdfplumber, pypdf, PyPDF2).")

if __name__ == "__main__":
    pdf = "proyecto.pdf"
    txt = "proyecto_text.txt"
    extract_pdf_text(pdf, txt)
