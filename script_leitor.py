import os
import pdfplumber
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))

pasta_pdfs = os.path.join(base_dir, "PDFs")
os.makedirs(pasta_pdfs, exist_ok=True)

pasta_saida = os.path.join(base_dir, "txt_extraidos")
os.makedirs(pasta_saida, exist_ok=True)

pdfs = [f for f in os.listdir(pasta_pdfs) if f.lower().endswith(".pdf")]

if not pdfs:
    print("🚫 Nenhum PDF encontrado na pasta 'PDFs'.")