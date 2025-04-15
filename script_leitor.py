import os
import pdfplumber
import tkinter as tk
from tkinter import messagebox

base_dir = os.path.dirname(os.path.abspath(__file__))
pasta_pdfs = os.path.join(base_dir, "PDFs")
pasta_saida = os.path.join(base_dir, "txt_extraidos")

os.makedirs(pasta_pdfs, exist_ok=True)
os.makedirs(pasta_saida, exist_ok=True)

def processar_pdfs():
    pdfs = [f for f in os.listdir(pasta_pdfs) if f.lower().endswith(".pdf")]

    if not pdfs:
        messagebox.showerror("Erro", "Nenhum PDF encontrado na pasta 'PDFs'.")
        return

    for pdf in pdfs:
        nome_pdf = os.path.splitext(pdf)[0]
        caminho_pdf = os.path.join(pasta_pdfs, pdf)
        caminho_txt = os.path.join(pasta_saida, f"{nome_pdf}.txt")

        try:
            with pdfplumber.open(caminho_pdf) as pdf_arquivo:
                texto_total = ""
                for pagina in pdf_arquivo.pages:
                    texto = pagina.extract_text()
                    if texto:
                        texto_total += texto + "\n"

            with open(caminho_txt, "w", encoding="utf-8") as txt_arquivo:
                txt_arquivo.write(texto_total)

            print(f"✅ Texto salvo em: {caminho_txt}")
            os.startfile(caminho_txt)

        except Exception as e:
            print(f"❌ Erro ao processar {pdf}: {e}")

root = tk.Tk()
root.withdraw()

resposta = messagebox.askyesno("Iniciar Leitura", "Deseja iniciar a leitura dos PDFs da pasta 'PDFs'?")
if resposta:
    processar_pdfs()

root.destroy()
