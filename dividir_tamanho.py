import os
import pikepdf
import io

step_pages = 15

def split_pdf_by_size(file_path, output_folder, max_size_mb, step):
    """
    Divide um arquivo PDF em partes sem exceder o tamanho máximo em megabytes.
    Utiliza processamento em lotes para eliminar lentidão.

    :param file_path: Caminho para o arquivo PDF de entrada.
    :param output_folder: Pasta onde os PDFs divididos serão salvos.
    :param max_size_mb: Tamanho máximo de cada parte em MB.
    :param step: Quantidade de páginas a processar antes de calcular o tamanho (Otimização).
    """
    max_size_bytes = max_size_mb * 1024 * 1024

    print(f"[INFO] Tentando abrir PDF: {file_path}")
    try:
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
    pdf_destino = pikepdf.Pdf.new()
    buffer = io.BytesIO()

    i = 0
    start_index = 0 # Guarda o índice de onde o PDF atual começou

    try:
        while i < total_pages:
            page_origem = pdf_origem.pages[i]
            pdf_destino.pages.append(page_origem)
            pages_added = len(pdf_destino.pages)
            
            print(f"[INFO] Processando página {i+1}/{total_pages} (Acumuladas no lote: {pages_added})...", end='\r')

            # OTIMIZAÇÃO MAX: Só compacta e checa o tamanho a cada 'step' páginas ou no final
            if pages_added % step == 0 or i == total_pages - 1:
                buffer.seek(0)
                buffer.truncate(0)
                pdf_destino.save(buffer)
                current_size = buffer.tell()

                if current_size > max_size_bytes:
                    print(f"\n[AVISO] Lote passou do limite ({current_size / 1024/1024:.2f} MB). Ajustando corte exato...")
                    
                    # RETROCESSO: Passou do limite, então apagamos 1 página por vez até o arquivo caber
                    while current_size > max_size_bytes and len(pdf_destino.pages) > 1:
                        del pdf_destino.pages[-1]
                        
                        buffer.seek(0)
                        buffer.truncate(0)
                        pdf_destino.save(buffer)
                        current_size = buffer.tell()

                    # Limite ideal encontrado, salva no disco!
                    output_filename = os.path.join(output_folder, f"parte_{part_number}.pdf")
                    pdf_destino.save(output_filename)
                    print(f"[OK] Gerado arquivo: {output_filename} ({current_size / 1024/1024:.2f} MB)")

                    saved_pages = len(pdf_destino.pages)
                    
                    # Atualiza os índices da leitura para recomeçar da página exata que não coube
                    i = start_index + saved_pages
                    start_index = i
                    part_number += 1
                    
                    # Cria PDF limpo para a próxima parte
                    pdf_destino = pikepdf.Pdf.new()
                    continue 

            i += 1

        # Salva qualquer página que restou quando o loop termina
        if len(pdf_destino.pages) > 0:
            buffer.seek(0)
            buffer.truncate(0)
            pdf_destino.save(buffer)
            current_size = buffer.tell()
            
            output_filename = os.path.join(output_folder, f"parte_{part_number}.pdf")
            pdf_destino.save(output_filename)
            print(f"\n[OK] Gerado arquivo final: {output_filename} ({current_size / 1024/1024:.2f} MB)")

    finally:
        pdf_origem.close()

    print("\n[FINALIZADO] Divisão por tamanho concluída.")

if __name__ == "__main__":
    arquivo_de_entrada = "Processos.pdf"
    pasta_de_saida = "pdfs"
    tamanho_maximo_mb = 18
    step_pages = 15

    split_pdf_by_size(arquivo_de_entrada, pasta_de_saida, max_size_mb=tamanho_maximo_mb, step=step_pages)