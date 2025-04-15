import os
import pdfplumber
import tkinter as tk
from tkinter import messagebox
import threading
import openai
import itertools
import time
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#openai.api_key = ""

base_dir = os.path.dirname(os.path.abspath(__file__))
pasta_pdfs = os.path.join(base_dir, "PDFs")
pasta_saida_extraidos = os.path.join(base_dir, "txt_extraidos")  
pasta_saida_resultado = os.path.join(base_dir, "Result_Analise")  

os.makedirs(pasta_pdfs, exist_ok=True)
os.makedirs(pasta_saida_extraidos, exist_ok=True)
os.makedirs(pasta_saida_resultado, exist_ok=True)

def analisar_com_gpt(texto):
    try:
        time.sleep(5) 
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente que analisa PDFs e entende qual é o tipo do conteúdo. Diga de forma direta e clara o que o texto representa."
                },
                {
                    "role": "user",
                    "content": f"Analise o seguinte texto extraído de um PDF:\n\n{texto[:3000]}"
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao analisar com IA: {e}"

def salvar_resultado_analise(nome_pdf, conteudo):
    caminho_analise = os.path.join(pasta_saida_resultado, f"{nome_pdf}_analise.txt")  
    with open(caminho_analise, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return caminho_analise

def mostrar_spinner_e_analisar(texto, nome_pdf):
    janela_spinner = tk.Toplevel()
    janela_spinner.title("Analisando com IA...")
    janela_spinner.geometry("300x150")

    label_mensagem = tk.Label(janela_spinner, text="Analisando, por favor aguarde...")
    label_mensagem.pack(pady=10)

    label_spinner = tk.Label(janela_spinner, font=("Courier", 18))
    label_spinner.pack()

    animando = True

    def animar():
        for frame in itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]):
            if not animando:
                break
            label_spinner.config(text=frame)
            time.sleep(0.1)

    thread_animacao = threading.Thread(target=animar)
    thread_animacao.start()

    def executar_analise():
        resultado = analisar_com_gpt(texto)
        caminho_analise = salvar_resultado_analise(nome_pdf, resultado)
        print(f"✅ Texto Analisado em: {os.path.abspath(caminho_analise)}")
        nonlocal animando
        animando = False
        janela_spinner.destroy()
        mostrar_resultado_final(resultado)

    threading.Thread(target=executar_analise).start()

def mostrar_resultado_final(texto):
    janela_final = tk.Toplevel()
    janela_final.title("Resultado Final da Análise")
    janela_final.geometry("600x400")
    tk.Label(janela_final, text="Resultado da Análise:", font=("Arial", 12, "bold")).pack(pady=10)
    texto_box = tk.Text(janela_final, wrap="word")
    texto_box.insert("1.0", texto)
    texto_box.config(state="disabled")
    texto_box.pack(expand=True, fill="both", padx=10, pady=10)

def mostrar_resultado_ia(texto_total, nome_pdf):
    janela_resultado = tk.Toplevel()
    janela_resultado.title("Análise da IA")
    janela_resultado.geometry("500x250")

    resumo = analisar_com_gpt(texto_total[:3000])
    tk.Label(janela_resultado, text=resumo, wraplength=450, pady=20, justify="left").pack()

    frame_botoes = tk.Frame(janela_resultado)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="✅ Confirmado", width=15,
              command=lambda: [janela_resultado.destroy(),
                               mostrar_spinner_e_analisar(texto_total, nome_pdf)]).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="❌ Negativo", width=15, command=janela_resultado.destroy).pack(side="right", padx=10)

def processar_pdfs():
    pdfs = [f for f in os.listdir(pasta_pdfs) if f.lower().endswith(".pdf")]

    if not pdfs:
        messagebox.showerror("Erro", "Nenhum PDF encontrado na pasta 'PDFs'.")
        return

    for pdf in pdfs:
        nome_pdf = os.path.splitext(pdf)[0]
        caminho_pdf = os.path.join(pasta_pdfs, pdf)
        caminho_txt = os.path.join(pasta_saida_extraidos, f"{nome_pdf}.txt")  

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

            thread_analise = threading.Thread(
                target=lambda: mostrar_resultado_ia(texto_total, nome_pdf)
            )
            thread_analise.start()

        except Exception as e:
            print(f"❌ Erro ao processar {pdf}: {e}")

root = tk.Tk()
root.withdraw()

resposta = messagebox.askyesno("Iniciar Leitura", "Deseja iniciar a leitura dos PDFs da pasta 'PDFs'?")
if resposta:
    processar_pdfs()

root.mainloop()
