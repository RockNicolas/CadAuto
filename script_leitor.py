import os
import tkinter as tk
from tkinter import messagebox
import threading
import itertools
import time
import pyautogui
import subprocess
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))
pasta_arquivos = os.path.join(base_dir, "Archives")
pasta_saida_resultado = os.path.join(base_dir, "Result_Analysis")
pasta_automacao = os.getenv("PASTA_AUTOMACAO")

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
    nome_base = os.path.splitext(nome_arquivo)[0]
    caminho_analise = os.path.join(pasta_saida_resultado, f"{nome_base}_analise.txt")
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
        time.sleep(5)  
        caminho_analise = salvar_resultado_analise(nome_arquivo, comentario)
        print(f"✅ Análise salva em: {os.path.abspath(caminho_analise)}")
        nonlocal animando
        animando = False
        janela_spinner.destroy()
        mostrar_resultado_final(comentario, nome_arquivo)

    threading.Thread(target=executar_analise).start()

def mostrar_resultado_final(texto, nome_arquivo):
    janela_final = tk.Toplevel()
    janela_final.title("Resultado Final da Análise")
    janela_final.geometry("600x300")  

    tk.Label(janela_final, text="Resultado da Análise:", font=("Arial", 12, "bold")).pack(pady=10)

    texto_box = tk.Text(janela_final, wrap="word", height=10, width=70)  
    texto_box.insert("1.0", texto)
    texto_box.config(state="disabled")
    texto_box.pack(expand=True, fill="both", padx=10, pady=10)
    botao_automacao = tk.Button(janela_final, text="Automação", command=lambda: automacao(nome_arquivo))
    botao_automacao.pack(pady=10)

#FOCO NA BUSCA
def automacao(nome_arquivo):
    caminho_pasta = pasta_arquivos

    if not os.path.exists(os.path.join(caminho_pasta, nome_arquivo)):
        messagebox.showerror("Erro", f"Arquivo {nome_arquivo} não encontrado na pasta de automação.")
        return

    subprocess.Popen(f'explorer "{caminho_pasta}"')
    time.sleep(3)

    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)

    nome_base = os.path.splitext(nome_arquivo)[0]
    pyautogui.write(nome_base[:100], interval=0.02)
    pyautogui.press('enter')  

    time.sleep(3)

    pyautogui.press('down')   
    time.sleep(0.5)
    pyautogui.press('enter')  
    time.sleep(0.5)
    pyautogui.press('enter')  #


def exibir_interface_de_resultados():
    janela_resultados = tk.Toplevel()
    janela_resultados.title("Arquivos para Análise")
    janela_resultados.geometry("600x400")

    frame_lista = tk.Frame(janela_resultados)
    frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

    arquivos = [f for f in os.listdir(pasta_arquivos) if os.path.isfile(os.path.join(pasta_arquivos, f))]

    if not arquivos:
        tk.Label(frame_lista, text="Nenhum arquivo encontrado na pasta 'Archives'.", fg="red").pack()
        return

    for arquivo in arquivos:
        linha = tk.Frame(frame_lista)
        linha.pack(fill="x", pady=5)

        label_nome = tk.Label(linha, text=arquivo, anchor="w")
        label_nome.pack(side="left", fill="x", expand=True)

        botao_analisar = tk.Button(linha, text="Analisar", command=lambda a=arquivo: mostrar_spinner_e_analisar(a))
        botao_analisar.pack(side="right")    

root = tk.Tk()
root.withdraw()

resposta = messagebox.askyesno("Iniciar Leitura", "Deseja iniciar a análise dos arquivos na pasta 'Archives'?")
if resposta:
    exibir_interface_de_resultados()

root.mainloop()
