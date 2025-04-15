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
else:
    for pdf in pdfs:
        nome_pdf = os.path.splitext(pdf)[0]
        caminho_pdf = os.path.join(pasta_pdfs, pdf)
        caminho_txt = os.path.join(pasta_saida, f"{nome_pdf}.txt")

    print(f"📄 Lendo: {pdf}")

    try:
        with pdfplumber.open(caminho_pdf) as pdf_arquivo:
            texto_total = ""
            for pagina in pdf_arquivo.pages:
                texto = pagina.extract_text()
                if texto:
                    texto_total += texto + "\n"

        with open(caminho_txt, "w", encoding="utf-8") as txt_arquivo:
            txt_arquivo.write(texto_total)

        print(f"✅ Texto salvo em: {caminho_txt}\n")

    except Exception as e:
        print(f"❌ Erro ao processar {pdf}: {e}")