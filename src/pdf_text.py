# src/pdf_text.py
"""
Simple PDF text extraction using PyMuPDF (fitz).
"""
import fitz  # PyMuPDF
import os
from typing import List, Tuple


def extract_text_from_pdf(path: str) -> str:
    """Extract full text from a single PDF file."""
    parts = []
    # Use context manager for safety
    with fitz.open(path) as doc:
        for page in doc:
            text = page.get_text("text")
            if text:
                parts.append(text)
    return "\n".join(parts)


def extract_texts_from_folder(folder_path: str, extensions: Tuple[str, ...] = (".pdf",)) -> List[Tuple[str, str, str]]:
    """
    Return list of (file_name, file_path, text) for each PDF in folder.
    If extraction fails, text will be "".
    """
    results: List[Tuple[str, str, str]] = []
    for fname in sorted(os.listdir(folder_path)):
        if fname.lower().endswith(extensions):
            fpath = os.path.join(folder_path, fname)
            try:
                text = extract_text_from_pdf(fpath)
            except Exception as e:
                print(f"❌ Error reading {fname}: {e}")
                text = ""
            results.append((fname, fpath, text))
    return results
