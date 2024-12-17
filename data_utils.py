import pdfplumber
import pandas as pd
import re

def extract_disease_data_from_pdf(pdf_path):
    disease_data = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                if re.match(r"^\d+\.\s", line):
                    disease_name = line.split(". ", 1)[-1]
                    disease_data[disease_name] = {"restricted": [], "recommendations": []}
    return disease_data

def load_excel_data(file_path):
    return pd.read_excel(file_path)
