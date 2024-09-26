from Getter_Functions import *

def get_bible_references():
    # Path to PDF file
    pdf_path: str = r'W:\Programming\The Christian in Complete Armou - William Gurnall.pdf'

    # Extract Text
    page_text: dict = extract_text_from_pdf(pdf_path)
    
    #Combine text to avoid errors when references go accross two pages
    combine_page_text = combine_text(page_text)
    
    bible_references: dict = bible_reference_regex(combine_page_text)
    
    for page_num, references in bible_references.items():
        for reference in references:
           print(f"Reference: {reference} - Page number: {page_num} \n")