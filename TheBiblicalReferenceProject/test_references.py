import unittest
import Bible_Reference_Getter

def expected_results() -> dict:
        # Expected answer file
        answer_path: str = r'C:\Users\16nat\source\repos\TheBiblicalReferenceProject\test_boiler_plate.txt'
        answer_references: dict = Bible_Reference_Getter.extract_text_from_pdf(answer_path)
        reference_expected: dict = Bible_Reference_Getter.bible_reference_regex(answer_references)
        return reference_expected

def test_file(test_path: str) -> dict:
    # Test function
    test_references: dict = Bible_Reference_Getter.extract_text_from_pdf(test_path)
    reference_results: dict = Bible_Reference_Getter.bible_reference_regex(test_references)
    
    return reference_results
    

class Test_Reference_Accuracy(unittest.TestCase):
    
    def test_normal_references(self):     
        # Test file
        normal_reference_path: str = r'C:\Users\16nat\source\repos\TheBiblicalReferenceProject\test_normal_references.txt'
        reference_results: dict = test_file(normal_reference_path)
        
        reference_expected: dict = expected_results()
        
        self.assertDictEqual(reference_results, reference_expected)
    
    def test_grouped_references(self):
        
        # Test file
        grouped_reference_path: str = r'C:\Users\16nat\source\repos\TheBiblicalReferenceProject\test_grouped_references.txt'
        reference_results: dict = test_file(grouped_reference_path)
        
        reference_expected: dict = expected_results()
        
        self.assertDictEqual(reference_results, reference_expected)
        
    
if __name__ == '__main__':
    unittest.main()