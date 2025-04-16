from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import filedialog

def analisar(nome_arquivo, pasta_arquivos):
    caminho = os.path.join(pasta_arquivos, nome_arquivo)
    
    img = Image.open(caminho)
    img.thumbnail((300, 300))  

    janela_imagem = tk.Toplevel()
    janela_imagem.title(f"Analisando {nome_arquivo}")
    
    largura, altura = 400, 400
    janela_imagem.geometry(f"{largura}x{altura}+{int(janela_imagem.winfo_screenwidth()/2 - largura/2)}+{int(janela_imagem.winfo_screenheight()/2 - altura/2)}")

    frame = tk.Frame(janela_imagem)
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_mensagem = tk.Label(frame, text=f"[Imagem] Arquivo '{nome_arquivo}' identificado como imagem.", justify="center")
    label_mensagem.pack(pady=10)

    img_tk = ImageTk.PhotoImage(img)
    label_imagem = tk.Label(frame, image=img_tk)
    label_imagem.image = img_tk 
    label_imagem.pack(pady=10)

    def editar_imagem():
        os.system(f"mspaint {caminho}")  

    botao_editar = tk.Button(frame, text="Editar Imagem", command=editar_imagem)
    botao_editar.pack(pady=10)

    janela_imagem.mainloop()

    return f"[Imagem] Arquivo '{nome_arquivo}' identificado como imagem. (Lógica de OCR ou metadados pode vir aqui)"
