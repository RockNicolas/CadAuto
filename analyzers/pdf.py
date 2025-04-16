import os

def analisar(nome_arquivo, pasta_arquivos):
    caminho = os.path.join(pasta_arquivos, nome_arquivo)
    return f"[PDF] Arquivo '{nome_arquivo}' analisado como PDF. (Lógica de leitura pode ser adicionada aqui)"
