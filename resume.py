from pypdf import PdfReader


def load_resume(pdf_path, output_path): 
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text

    with open(output_path, "w", encoding="utf-8") as f:
        print("Writing resume to file")
        f.write(text)
    return text
            
        