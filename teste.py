import os
import re

# Pasta com arquivos .txt de entrada
PASTA_ENTRADA = "Archives"
PASTA_SAIDA = "Result_Analysis"
ARQUIVO_SAIDA = os.path.join(PASTA_SAIDA, "resultado.txt")

# Cria pasta de saída se não existir
os.makedirs(PASTA_SAIDA, exist_ok=True)

def extrair_linhas_validas(texto):
    """
    Extrai linhas com 4 valores separados por espaço (no formato x,xx).
    """
    padrao = r"(\d+,\d+)\s+(\d+,\d+)\s+(\d+,\d+)\s+(\d+,\d+)"
    return re.findall(padrao, texto)

def processar_valores(linhas):
    estacas, ct, cp, p = [], [], [], []

    for i, (e, ct_val, cp_val, p_val) in enumerate(linhas):
        estacas.append(e)
        cp.append(cp_val)
        if i % 2 == 0:
            ct.append(ct_val)
            p.append(p_val)
        else:
            ct.append("")
            p.append("")

    # Intercalar 10,00 e 0,00 entre estacas
    nova_estacas = []
    for i, valor in enumerate(estacas):
        nova_estacas.append(valor)
        if i < len(estacas) - 1:
            nova_estacas.extend(["10,00", "0,00"])
    estacas = nova_estacas[:len(ct)]  # Garante o mesmo tamanho

    return estacas, ct, cp, p

def salvar_txt(nome_arquivo, estacas, ct, cp, p):
    with open(ARQUIVO_SAIDA, "a", encoding="utf-8") as f:
        f.write(f"\n🔹 Resultados do arquivo: {nome_arquivo}\n")
        f.write("ESTACAS\tCT\tCP\tP\n")
        for i in range(len(ct)):
            f.write(f"{estacas[i]}\t{ct[i]}\t{cp[i]}\t{p[i]}\n")
        f.write("-" * 40 + "\n")

def processar_arquivos_txt():
    encontrou = False
    for nome_arquivo in os.listdir(PASTA_ENTRADA):
        if nome_arquivo.lower().endswith(".txt"):
            caminho = os.path.join(PASTA_ENTRADA, nome_arquivo)
            with open(caminho, "r", encoding="utf-8") as f:
                texto = f.read()
            print(f"📄 Lendo arquivo: {nome_arquivo}")
            linhas = extrair_linhas_validas(texto)
            if linhas:
                estacas, ct, cp, p = processar_valores(linhas)
                salvar_txt(nome_arquivo, estacas, ct, cp, p)
                encontrou = True
            else:
                print(f"⚠️ Nenhum dado válido encontrado em: {nome_arquivo}")
    if encontrou:
        print(f"\n✅ Resultado salvo em: {ARQUIVO_SAIDA}")
    else:
        print("⚠️ Nenhum arquivo válido ou dados encontrados.")

# Executa o processo
processar_arquivos_txt()
