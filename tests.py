import unittest
import os
from nlp_cv_screening import extract_skills, preprocess_text, extract_text_from_pdf, assign_points

# Are skills extracted from the CSV?
class TestExtractSkills(unittest.TestCase):
    def test_extract_skills_from_cvs(self):
        skills_path = "CV_Screening_Skills.csv" 
        skills = extract_skills(skills_path)
        self.assertTrue(len(skills) > 0, "Not all skills processed.")

# Is text extracted from the CVs?
class TestCVProcessing(unittest.TestCase):
    def test_extract_text_from_pdf(self):
        cv_folder = "CVs" 
        for filename in os.listdir(cv_folder):
            if filename.endswith(".pdf"):
                cv_path = os.path.join(cv_folder, filename)
                extracted_text = extract_text_from_pdf(cv_path)
                self.assertTrue(extracted_text, f"No text extracted from {filename}.")

if __name__ == '__main__':
    unittest.main()