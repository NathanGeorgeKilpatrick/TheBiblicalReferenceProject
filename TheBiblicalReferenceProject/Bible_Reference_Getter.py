from Getter_Functions import *

def get_bible_references():
    # Path to PDF file
    pdf_path: str = r'W:\Programming\365_Bible_Verses(1).pdf'

    # Extract Text
    all_text, page_ranges = extract_text_from_pdf(pdf_path)
    
    bible_references: dict = bible_reference_regex(all_text, page_ranges)
    
    for page_num, references in bible_references.items():
        for reference in references:
           print(f"Reference: {reference} - Page number: {page_num} \n")