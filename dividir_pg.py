import os
import pikepdf

#VARIAVÉIS PARA ALTERAR
pg = 30
pasta = "pdfs"
pdf = "processos.pdf"

def split_pdf(file_path, output_folder, chunk_size=pg):
    print(f"[INFO] Tentando abrir PDF: {file_path}")
    try:
        pdf = pikepdf.open(file_path)
    except Exception as e:
        print(f"[ERRO] Não consegui abrir o PDF: {e}")
        return
    
    total_pages = len(pdf.pages)
    print(f"[INFO] PDF aberto com sucesso. Total de páginas: {total_pages}")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"[INFO] Pasta de saída criada: {output_folder}")

    part_number = 1
    for i in range(0, total_pages, chunk_size):
        print(f"[INFO] Processando páginas {i+1} até {min(i + chunk_size, total_pages)}...")
        try:
            new_pdf = pikepdf.Pdf.new()
            for j in range(i, min(i + chunk_size, total_pages)):
                new_pdf.pages.append(pdf.pages[j])
            
            output_filename = os.path.join(output_folder, f"parte_{part_number}.pdf")
            new_pdf.save(output_filename)
            print(f"[OK] Gerado arquivo: {output_filename}")
            part_number += 1
        except Exception as e:
            print(f"[ERRO] Falhou ao salvar parte {part_number}: {e}")
            continue

    print("[FINALIZADO] Divisão concluída.")

split_pdf(pdf, pasta, chunk_size=pg)
