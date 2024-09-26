import fitz # PyMuPDF
import PyPDF2
import re


import Bible_Book_Dictionary

# The function is formatted like this so that if references span across two pages they can sill be found by regex.
# It also allows to keep track of what pages the references were found on by referenceing the index of the reference
# to the page ranges
def extract_text_from_pdf(pdf_path: str) -> tuple[str, dict[int, int]]:
    """    
    A function that extracts text from a PDF file, using the pdf_path string variable to find the document
    within the system. 
    It then extracts the text then combines the text into on string, it records the pages in a dictionary.
    
    Args:
        pdf_path (str): This is the path to the pdf file yo want to extract

    Returns:
        tuple[str, dict[int, int]]: This returns two values all the text in the document as a string and a dictionary containing page numbers for the document
    """

    with open(pdf_path, 'rb') as pdf_document:
        
        reader = PyPDF2.PdfReader(pdf_document, strict=False)
        all_text: str = ""
        page_ranges: dict[int, tuple[int, int]] = {}
        current_position = 0
        i = 1

        for page in reader.pages:
            content = page.extract_text()
            all_text += content
            
            page_start = current_position
            current_position += len(content)
            page_end = current_position
            page_ranges[i] = (page_start, page_end)
            i += 1        

        return all_text, page_ranges
    
def bible_reference_regex(page_text: str, page_ranges: dict ) -> dict:
    """
    A function that uses Regex pattern searching for bible references in text. 
    The parameter for the text is using a dictionary where the key is the page number and the value is the text of that page.
    The function will return a dictionary of references by their page number.

    Args:
        text_by_page (dict): A dictionary of text and page numbers. Where the page numbers is the key and the text is the value.

    Returns:
        dict: A dictionary of page numbers (keys) and the corrisponding bible references (values)
        
    """
    regex_pattern: str = r'\b(?:I{0,3}?\s?\b(?:[A-Za-z]+))?.\s\d{1,3}:\d{1,3}(?:-\d{1,3})?\b'
    references_by_page: dict = {}
    
    for page_num, text in page_text.items():
        # Finds the references and cleans them up for future use. 
        references_search: str = re.findall(regex_pattern, text.replace("\n", "").replace("\r", ""))
        if references_search:
            for index, reference in enumerate(references_search):
                
                if "." in reference:
                    index_of_full_stop: int = reference.find(".")
                    if index_of_full_stop != -1:
                        i = 0
                        for char in reference:
                            if char.islower():
                                i += 1
                            else:
                                break
                            
                        abbr_text: str = reference[i:reference.find(".")].replace(" ", "")
                        if abbr_text in Bible_Book_Dictionary.bible_books_with_abbreviations:
                            text_after_full_stop: str = reference[index_of_full_stop + 1]
                            new_text: str = Bible_Book_Dictionary.bible_books_with_abbreviations[abbr_text]
                            new_string: str = new_text + text_after_full_stop
                            references_search[index] = new_string
            references_by_page[page_num] = references_search
    return references_by_page
     
                