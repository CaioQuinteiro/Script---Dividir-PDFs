import os
import pikepdf
import tempfile

def split_pdf_by_size(file_path, output_folder, max_size_mb=10):
    """
    Divide um arquivo PDF em partes, garantindo que cada parte
    não exceda um tamanho máximo em megabytes.

    :param file_path: Caminho para o arquivo PDF de entrada.
    :param output_folder: Pasta onde os PDFs divididos serão salvos.
    :param max_size_mb: Tamanho máximo de cada parte em MB.
    """
    max_size_bytes = max_size_mb * 1024 * 1024

    print(f"[INFO] Tentando abrir PDF: {file_path}")
    try:
        # Abre o PDF original
        pdf_origem = pikepdf.open(file_path)
    except Exception as e:
        print(f"[ERRO] Não consegui abrir o PDF: {e}")
        return

    total_pages = len(pdf_origem.pages)
    print(f"[INFO] PDF aberto. Páginas: {total_pages}. Limite por parte: {max_size_mb} MB.")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"[INFO] Pasta de saída criada: {output_folder}")

    part_number = 1
    # Cria o primeiro PDF de destino
    pdf_destino = pikepdf.Pdf.new()
    
    # Cria um nome de arquivo temporário seguro
    temp_fd, temp_filename = tempfile.mkstemp(suffix=".pdf")
    os.close(temp_fd)

    try:
        for i, page_origem in enumerate(pdf_origem.pages):
            print(f"[INFO] Processando página {i+1}/{total_pages}...")
            
            # --- CORREÇÃO PRINCIPAL APLICADA AQUI ---
            # Copia a página do PDF de origem para o de destino.
            # Isso evita o erro de referência a um PDF "destruído".
            pdf_destino.pages.append(page_origem)
            # --- FIM DA CORREÇÃO ---
            
            # Salva o estado atual para verificar o tamanho
            pdf_destino.save(temp_filename)
            current_size = os.path.getsize(temp_filename)

            # 1. Checa se UMA ÚNICA página já estoura o limite
            if len(pdf_destino.pages) == 1 and current_size > max_size_bytes:
                print(f"[AVISO] A página {i+1} sozinha ({current_size / 1024/1024:.2f} MB) já excede o limite de {max_size_mb} MB.")
                output_filename = os.path.join(output_folder, f"parte_{part_number}.pdf")
                pdf_destino.save(output_filename)
                print(f"[OK] Arquivo (acima do limite) gerado: {output_filename}")
                
                part_number += 1
                pdf_destino = pikepdf.Pdf.new() # Começa um novo PDF de destino, limpo
                continue

            # 2. Checa se a adição da nova página estourou o limite (cenário normal)
            if current_size > max_size_bytes:
                print(f"[AVISO] Tamanho excedido ({current_size / 1024/1024:.2f} MB). Finalizando parte {part_number}.")
                
                # Remove a última página (que causou o excesso) do PDF de destino
                del pdf_destino.pages[-1]
                
                # Salva o PDF (agora dentro do limite)
                output_filename = os.path.join(output_folder, f"parte_{part_number}.pdf")
                pdf_destino.save(output_filename)
                print(f"[OK] Gerado arquivo: {output_filename}")
                
                # Inicia a próxima parte
                part_number += 1
                pdf_destino = pikepdf.Pdf.new() # Cria um novo PDF de destino
                # Adiciona a página que foi removida (page_origem) como a primeira do novo PDF
                pdf_destino.pages.append(page_origem)

        # Salva a última parte que sobrou após o fim do loop
        if len(pdf_destino.pages) > 0:
            output_filename = os.path.join(output_folder, f"parte_{part_number}.pdf")
            pdf_destino.save(output_filename)
            print(f"[OK] Gerado arquivo final: {output_filename}")

    finally:
        # Garante que o arquivo temporário e o PDF original sejam fechados
        pdf_origem.close()
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            print("[INFO] Arquivo temporário removido.")

    print("\n[FINALIZADO] Divisão por tamanho concluída.")


# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    arquivo_de_entrada = "Processos.pdf"
    pasta_de_saida = "saidas"
    tamanho_maximo_mb = 10

    split_pdf_by_size(arquivo_de_entrada, pasta_de_saida, max_size_mb=tamanho_maximo_mb)