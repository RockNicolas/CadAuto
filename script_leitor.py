import os
import tkinter as tk
from tkinter import messagebox
import threading
import itertools
import time
import pyautogui
import subprocess
from dotenv import load_dotenv
from analyzers import pdf, imagem

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))
pasta_arquivos = os.path.join(base_dir, "Archives")
pasta_saida_resultado = os.path.join(base_dir, "Result_Analysis")
pasta_automacao = os.getenv("PASTA_AUTOMACAO")

os.makedirs(pasta_arquivos, exist_ok=True)
os.makedirs(pasta_saida_resultado, exist_ok=True)

def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def analisar_tipo_arquivo(nome_arquivo):
    ext = os.path.splitext(nome_arquivo)[1].lower()

    if ext == ".pdf":
        return pdf.analisar(nome_arquivo, pasta_arquivos)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return imagem.analisar(nome_arquivo, pasta_arquivos)
    else:
        return('tipo de arquivo não encontrado.')

def salvar_resultado_analise(nome_arquivo, conteudo):
    nome_base = os.path.splitext(nome_arquivo)[0]
    caminho_analise = os.path.join(pasta_saida_resultado, f"{nome_base}_analise.txt")
    with open(caminho_analise, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return caminho_analise

def mostrar_resultado_final(texto, nome_arquivo):
    janela_final = tk.Toplevel()
    janela_final.title("Resultado Final da Análise")
    centralizar_janela(janela_final, 600, 300)

    container = tk.Frame(janela_final)
    container.pack(expand=True, fill="both", padx=10, pady=10)

    tk.Label(container, text="Resultado da Análise:", font=("Arial", 12, "bold"), anchor="center").pack(pady=10)

    texto_box = tk.Text(container, wrap="word", height=10, width=70)
    texto_box.insert("1.0", texto)
    texto_box.config(state="disabled")
    texto_box.pack(expand=True, fill="both", pady=10)

def mostrar_spinner_e_analisar(nome_arquivo):
    for widget in tk._default_root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()

    janela_spinner = tk.Toplevel()
    janela_spinner.title("Abrindo Arquivo...")
    centralizar_janela(janela_spinner, 300, 150)

    frame = tk.Frame(janela_spinner)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    label_mensagem = tk.Label(frame, text="Analisando arquivo, por favor aguarde...", justify="center")
    label_mensagem.pack(pady=10)

    label_spinner = tk.Label(frame, font=("Courier", 18))
    label_spinner.pack(pady=10)

    animando = True

    def animar():
        for frame in itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]):
            if not animando:
                break
            label_spinner.config(text=frame)
            time.sleep(0.1)

    threading.Thread(target=animar, daemon=True).start()

    def executar_analise():
        comentario = analisar_tipo_arquivo(nome_arquivo)
        salvar_resultado_analise(nome_arquivo, comentario)

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

        time.sleep(1.5)
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('enter')
        time.sleep(20)

        nonlocal animando
        animando = False
        janela_spinner.destroy()
        mostrar_resultado_final(comentario, nome_arquivo)

    threading.Thread(target=executar_analise, daemon=True).start()

def exibir_interface_de_resultados():
    janela_resultados = tk.Toplevel()
    janela_resultados.title("Arquivos para Análise")
    centralizar_janela(janela_resultados, 600, 400)

    frame_lista = tk.Frame(janela_resultados)
    frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

    arquivos = [f for f in os.listdir(pasta_arquivos) if os.path.isfile(os.path.join(pasta_arquivos, f))]

    if not arquivos:
        tk.Label(frame_lista, text="Nenhum arquivo encontrado na pasta 'Archives'.", fg="red").pack(pady=20)
        return

    for arquivo in arquivos:
        linha = tk.Frame(frame_lista)
        linha.pack(fill="x", pady=5)

        label_nome = tk.Label(linha, text=arquivo, anchor="center", width=50)
        label_nome.pack(side="left", fill="x", padx=5)

        botao_analisar = tk.Button(linha, text="Analisar", width=10, command=lambda a=arquivo: mostrar_spinner_e_analisar(a))
        botao_analisar.pack(side="right", padx=5)

root = tk.Tk()
root.withdraw()

resposta = messagebox.askyesno("Iniciar Leitura", "Deseja iniciar a análise dos arquivos na pasta 'Archives'?")
if resposta:
    exibir_interface_de_resultados()

root.mainloop()
