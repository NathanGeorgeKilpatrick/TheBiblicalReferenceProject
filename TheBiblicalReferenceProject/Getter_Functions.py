import fitz # PyMuPDF
import re


import Bible_Book_Dictionary

def extract_text_from_pdf(pdf_path: str) -> dict[int, str]:
    """
    A function that extracts text from a PDF file, using the pdf_path string variable to find the document
    within the system. 
    This functino will then return a dictionary with page numbers as keys.
    
    Args:
        pdf_path (str): A string using the file path to the pdf file whos text needs to be extracted.

    Returns:
        dict: Returning a dictionary where - 'Key' : 'Value' - 'Page number' : 'Page text'
    """
    
    with open(pdf_path, 'r') as pdf_document:

        text_by_page: dict = {}

        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text = page.get_text()
            text_by_page[page_num + 1] = text

        return text_by_page
    
def combine_text(page_text: dict) -> tuple[str, dict[int, tuple[int, int]]]:
    """
    A function that combines the text in a document and returns a multipage document as a single string.
    The function also saves the the page numbers, so that the user can know what page a particular references was found on.

    Args:
        page_text (dict):  

    Returns:
        tuple[str, dict]: _description_
    """
    output = ""
    page_ranges = {}
    current_position = 0
    
    # This find and stores the start and end of the page making it possible to 
    # combine the text and still store the page the references was found at
    for page_num, text in page_text.items():
        page_start = current_position
        output += text.replace('\n', ' ')
        current_position += len(text)
        page_end = current_position
        page_ranges[page_num] = (page_start, page_end)
    
    return output, page_ranges
    
def bible_reference_regex(Page_text: str) -> dict:
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
    
    for page_num, text in text_by_page.items():
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
     
                