import os

def limpar_pasta(caminho_pasta):

    if not os.path.isdir(caminho_pasta):
        print(f"[AVISO] A pasta '{caminho_pasta}' não existe. Nada a fazer.")
        return

    print(f"[INFO] Limpando a pasta: {caminho_pasta}")

    arquivos_na_pasta = os.listdir(caminho_pasta)

    if not arquivos_na_pasta:
        print("[INFO] A pasta já está vazia.")
        return

    for nome_arquivo in arquivos_na_pasta:
        caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
        try:
            if os.path.isfile(caminho_completo):
                os.remove(caminho_completo)
                print(f"[OK] Arquivo deletado: {nome_arquivo}")
            else:
                print(f"[AVISO] '{nome_arquivo}' é uma pasta, não será deletado.")
        except Exception as e:
            print(f"[ERRO] Não foi possível deletar o arquivo {nome_arquivo}: {e}")
    
    print("\n[FINALIZADO] Limpeza concluída.")

pasta_para_limpar = "pdfs"

limpar_pasta(pasta_para_limpar)