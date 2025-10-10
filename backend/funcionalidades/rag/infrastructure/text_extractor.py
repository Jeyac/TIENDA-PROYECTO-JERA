import io
import os
from typing import Tuple

from pdfminer.high_level import extract_text as pdf_extract_text


class TextExtractor:
    @staticmethod
    def from_file(storage) -> Tuple[str, str]:
        """Devuelve (titulo, contenido) a partir de un archivo subido."""
        filename = storage.filename or 'documento'
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.pdf':
            content = pdf_extract_text(storage.stream)
            title = os.path.splitext(filename)[0]
            return title, content
        if ext in ('.md', '.txt'):
            content = storage.stream.read().decode('utf-8', errors='ignore')
            title = os.path.splitext(filename)[0]
            return title, content
        # fallback: intenta tratar como texto
        content = storage.stream.read().decode('utf-8', errors='ignore')
        title = os.path.splitext(filename)[0]
        return title, content






