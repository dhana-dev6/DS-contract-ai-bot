import io
import pdfplumber
import docx

def extract_text_from_pdf(file_bytes):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            if not pdf.pages:
                return "Error: The PDF file seems empty or has no pages."
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        if not text.strip():
            return "Warning: No text could be extracted from this PDF. It might be an image-only scan."
    except Exception as e:
        # Catch structurally invalid PDFs
        return f"Error: Unable to parse PDF. The file might be corrupted or not a valid PDF. Details: {str(e)}"
    return text

def extract_text_from_docx(file_bytes):
    """Extracts text from a DOCX file."""
    doc = docx.Document(io.BytesIO(file_bytes))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_txt(file_bytes):
    """Extracts text from a TXT file."""
    return file_bytes.decode("utf-8")

def parse_document(uploaded_file):
    """
    Dispatcher function to parse uploaded files based on extension.
    Args:
        uploaded_file: Streamlit UploadedFile object
    Returns:
        str: Extracted text
    """
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    if file_extension == "pdf":
        return extract_text_from_pdf(uploaded_file.getvalue())
    elif file_extension in ["docx", "doc"]:
        return extract_text_from_docx(uploaded_file.getvalue())
    elif file_extension == "txt":
        return extract_text_from_txt(uploaded_file.getvalue())
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
