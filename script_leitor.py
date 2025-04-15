import os
import tkinter as tk
from tkinter import messagebox
import threading
import itertools
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
pasta_arquivos = os.path.join(base_dir, "Archives")
pasta_saida_resultado = os.path.join(base_dir, "Result_Analysis")

os.makedirs(pasta_arquivos, exist_ok=True)
os.makedirs(pasta_saida_resultado, exist_ok=True)

def analisar_tipo_arquivo(nome_arquivo):
    ext = os.path.splitext(nome_arquivo)[1].lower()
    if ext == ".pdf":
        return "Este é um arquivo PDF, possivelmente um documento de texto."
    elif ext in [".xls", ".xlsx"]:
        return "Este é um arquivo Excel, geralmente utilizado para planilhas."
    elif ext == ".dwg":
        return "Este é um arquivo DWG, comumente usado em projetos do AutoCAD."
    elif ext in [".jpg", ".jpeg", ".png"]:
        return "Este é um arquivo de imagem (JPG/PNG)."
    elif ext in [".doc", ".docx"]:
        return "Este é um arquivo Word, usado para documentos de texto formatados."
    elif ext in [".txt"]:
        return "Este é um arquivo de texto simples (.txt)."
    else:
        return f"Tipo de arquivo '{ext}' não reconhecido com precisão."

def salvar_resultado_analise(nome_arquivo, conteudo):
    caminho_analise = os.path.join(pasta_saida_resultado, f"{nome_arquivo}_analise.txt")
    with open(caminho_analise, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return caminho_analise

def mostrar_spinner_e_analisar(nome_arquivo):
    janela_spinner = tk.Toplevel()
    janela_spinner.title("Analisando Arquivo...")
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

    threading.Thread(target=animar).start()

    def executar_analise():
        comentario = analisar_tipo_arquivo(nome_arquivo)
        time.sleep(10) 
        caminho_analise = salvar_resultado_analise(nome_arquivo, comentario)
        print(f"✅ Análise salva em: {os.path.abspath(caminho_analise)}")
        nonlocal animando
        animando = False
        janela_spinner.destroy()
        mostrar_resultado_final(comentario)

    threading.Thread(target=executar_analise).start()

def mostrar_resultado_final(texto):
    janela_final = tk.Toplevel()
    janela_final.title("Resultado Final da Análise")
    janela_final.geometry("600x200")
    tk.Label(janela_final, text="Resultado da Análise:", font=("Arial", 12, "bold")).pack(pady=10)
    texto_box = tk.Text(janela_final, wrap="word")
    texto_box.insert("1.0", texto)
    texto_box.config(state="disabled")
    texto_box.pack(expand=True, fill="both", padx=10, pady=10)

def processar_arquivos():
    arquivos = [f for f in os.listdir(pasta_arquivos) if os.path.isfile(os.path.join(pasta_arquivos, f))]

    if not arquivos:
        messagebox.showerror("Erro", "Nenhum arquivo encontrado na pasta 'Archives'.")
        return

    for arquivo in arquivos:
        def iniciar_thread(arquivo_local):
            thread = threading.Thread(target=lambda: mostrar_spinner_e_analisar(arquivo_local))
            thread.start()

        iniciar_thread(arquivo)

root = tk.Tk()
root.withdraw()

resposta = messagebox.askyesno("Iniciar Leitura", "Deseja iniciar a análise dos arquivos na pasta 'Archives'?")
if resposta:
    processar_arquivos()

root.mainloop()
