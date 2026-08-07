import os
from pypdf import PdfWriter

def mesclar_pdfs(pasta_origem, arquivo_saida):
    # Cria o objeto que vai juntar os PDFs
    merger = PdfWriter()
    
    # Lista todos os arquivos da pasta que terminam em .pdf
    arquivos_pdf = [arquivo for arquivo in os.listdir(pasta_origem) if arquivo.lower().endswith('.pdf')]
    
    # Ordena os arquivos em ordem alfabética (opcional, mas recomendado)
    arquivos_pdf.sort()
    
    if not arquivos_pdf:
        print("Nenhum arquivo PDF encontrado nessa pasta.")
        return

    # Percorre cada arquivo PDF encontrado
    for arquivo in arquivos_pdf:
        caminho_completo = os.path.join(pasta_origem, arquivo)
        merger.append(caminho_completo)
        print(f"Adicionado: {arquivo}")
        
    # Salva o resultado final no arquivo de saída
    with open(arquivo_saida, "wb") as saida:
        merger.write(saida)
        
    print(f"\nSucesso! Todos os PDFs foram mesclados em: {arquivo_saida}")


pasta_dos_pdfs = "./pdfs" 

nome_do_arquivo_final = "pdf_completo.pdf"

mesclar_pdfs(pasta_dos_pdfs, nome_do_arquivo_final)