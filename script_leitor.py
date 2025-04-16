import os
import tkinter as tk
import threading
import time
import pyautogui
import subprocess
from tkinter import ttk
from tkinter import messagebox
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))
pasta_arquivos = os.path.join(base_dir, "Archives")
pasta_saida_resultado = os.path.join(base_dir, "Result_Analysis")
pasta_automacao = os.getenv("PASTA_AUTOMACAO")

os.makedirs(pasta_arquivos, exist_ok=True)
os.makedirs(pasta_saida_resultado, exist_ok=True)

janela_atual = None

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
        return f"O arquivo '{nome_arquivo}' é um PDF. (Análise simulada)"
    elif ext in [".jpg", ".jpeg", ".png"]:
        return f"O arquivo '{nome_arquivo}' é uma imagem. (Análise simulada)"
    elif ext in [".dwg"]:
        return f"O arquivo '{nome_arquivo}' é um desenho técnico DWG. (Análise simulada)"
    elif ext in [".xls", ".xlsx"]:
        return f"O arquivo '{nome_arquivo}' é uma planilha Excel. (Análise simulada)"
    else:
        return 'Tipo de arquivo não reconhecido.'

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
    janela_final.configure(bg="#f2f2f2")

    container = tk.Frame(janela_final, bg="#f2f2f2")
    container.pack(expand=True, fill="both", padx=10, pady=10)

    tk.Label(container, text="Resultado da Análise:", font=("Arial", 14, "bold"), anchor="center", bg="#f2f2f2", fg="#333").pack(pady=10)

    texto_box = tk.Text(container, wrap="word", height=10, width=70, font=("Arial", 10), bg="#fff", fg="#333", bd=2, relief="groove")
    texto_box.insert("1.0", texto)
    texto_box.config(state="disabled")
    texto_box.pack(expand=True, fill="both", pady=10)

def mostrar_barra_de_progresso_e_analisar(caminho_completo, nome_arquivo):
    for widget in tk._default_root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()

    janela_spinner = tk.Toplevel()
    janela_spinner.title("Abrindo Arquivo...")
    centralizar_janela(janela_spinner, 300, 150)
    janela_spinner.configure(bg="#f2f2f2")

    frame = tk.Frame(janela_spinner, bg="#f2f2f2")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    label_mensagem = tk.Label(frame, text="Analisando arquivo, por favor aguarde...", justify="center", bg="#f2f2f2", fg="#333", font=("Arial", 10))
    label_mensagem.pack(pady=10)

    barra_progresso = ttk.Progressbar(frame, length=200, mode='determinate')
    barra_progresso.pack(pady=10)
    barra_progresso['value'] = 0 

    def atualizar_barra(progresso):
        barra_progresso['value'] = progresso
        janela_spinner.update_idletasks()

    def executar_analise():
        comentario = analisar_tipo_arquivo(nome_arquivo)
        salvar_resultado_analise(nome_arquivo, comentario)

        
        for i in range(101):
            time.sleep(0.1)  
            atualizar_barra(i)

   
        if not os.path.exists(caminho_completo):
            messagebox.showerror("Erro", f"Arquivo {nome_arquivo} não encontrado.")
            return

        subprocess.Popen(f'explorer "{os.path.dirname(caminho_completo)}"')
        time.sleep(2) 

        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.8)  
        nome_base = os.path.splitext(nome_arquivo)[0]
        pyautogui.write(nome_base[:100], interval=0.02)
        time.sleep(1)
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('enter')

        time.sleep(1)
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('enter')

        janela_spinner.after(0, lambda: janela_spinner.destroy())
        janela_spinner.after(0, lambda: mostrar_resultado_final(comentario, nome_arquivo))

    threading.Thread(target=executar_analise, daemon=True).start()

def exibir_interface_de_arquivos(subpasta_path):
    global janela_atual
    if janela_atual and janela_atual.winfo_exists():
        janela_atual.destroy()

    janela_arquivos = tk.Toplevel()
    janela_arquivos.title(f"Arquivos de: {os.path.basename(subpasta_path)}")
    centralizar_janela(janela_arquivos, 600, 400)
    janela_arquivos.configure(bg="#f2f2f2")
    janela_atual = janela_arquivos

    topo = tk.Frame(janela_arquivos, bg="#f2f2f2")
    topo.pack(fill="x", padx=10, pady=(10, 0))

    botao_voltar = tk.Button(topo, text="<", command=exibir_interface_de_pastas, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised", bd=2)
    botao_voltar.pack(side="left", anchor="w", padx=5)

    frame_lista = tk.Frame(janela_arquivos, bg="#f2f2f2")
    frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

    arquivos = [f for f in os.listdir(subpasta_path) if os.path.isfile(os.path.join(subpasta_path, f))]

    if not arquivos:
        tk.Label(frame_lista, text="Nenhum arquivo encontrado nesta pasta.", fg="red", bg="#f2f2f2").pack(pady=20)
        return

    for arquivo in arquivos:
        linha = tk.Frame(frame_lista, bg="#f2f2f2")
        linha.pack(fill="x", pady=5)

        label_nome = tk.Label(linha, text=arquivo, anchor="center", width=50, bg="#f2f2f2", font=("Arial", 12))
        label_nome.pack(side="left", fill="x", padx=5)

        caminho_completo = os.path.join(subpasta_path, arquivo)
        botao_analisar = tk.Button(linha, text="Analisar", width=10, command=lambda c=caminho_completo, a=arquivo: mostrar_barra_de_progresso_e_analisar(c, a), bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised", bd=2)
        botao_analisar.pack(side="right", padx=5)

def exibir_interface_de_pastas():
    global janela_atual
    if janela_atual and janela_atual.winfo_exists():
        janela_atual.destroy()

    janela_pastas = tk.Toplevel()
    janela_pastas.title("Pastas para Análise")
    centralizar_janela(janela_pastas, 600, 400)
    janela_pastas.configure(bg="#f2f2f2")
    janela_atual = janela_pastas

    frame_lista = tk.Frame(janela_pastas, bg="#f2f2f2")
    frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

    subpastas = [d for d in os.listdir(pasta_arquivos) if os.path.isdir(os.path.join(pasta_arquivos, d))]

    if not subpastas:
        tk.Label(frame_lista, text="Nenhuma subpasta encontrada na pasta 'Archives'.", fg="red", bg="#f2f2f2").pack(pady=20)
        return

    for subpasta in subpastas:
        linha = tk.Frame(frame_lista, bg="#f2f2f2")
        linha.pack(fill="x", pady=5)

        label_nome = tk.Label(linha, text=subpasta, anchor="center", width=50, bg="#f2f2f2", font=("Arial", 12))
        label_nome.pack(side="left", fill="x", padx=5)

        caminho_subpasta = os.path.join(pasta_arquivos, subpasta)
        botao_abrir = tk.Button(linha, text="Abrir", width=10, command=lambda c=caminho_subpasta: exibir_interface_de_arquivos(c), bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised", bd=2)
        botao_abrir.pack(side="right", padx=5)

root = tk.Tk()
root.withdraw()

resposta = messagebox.askyesno("Iniciar Leitura", "Deseja iniciar a análise das pastas na 'Archives'?")
if resposta:
    exibir_interface_de_pastas()

root.mainloop()
