import PyPDF2
import sys
import os

def obter_local_do_exe():
    # Retorna a pasta onde o .exe (ou o script) está localizado
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def processar_pdf(caminho_arquivo):
    # Limpa o caminho do arquivo arrastado
    caminho_arquivo = caminho_arquivo.strip(' "')
    
    if not os.path.exists(caminho_arquivo):
        print(f"❌ Erro: Arquivo não encontrado.")
        return

    try:
        print("\n--- Configuração de Páginas ---")
        inicio = int(input("Inserir folha em branco APÓS qual página? (Ex: 3): "))
        intervalo = int(input("De quantas em quantas páginas pular? (Ex: 3): "))
        
        reader = PyPDF2.PdfReader(caminho_arquivo)
        writer = PyPDF2.PdfWriter()
        total_paginas = len(reader.pages) 

        # --- LÓGICA DE PASTA LOCAL ---
        # Cria a pasta 'arquivos' no mesmo local do executável
        pasta_exe = obter_local_do_exe()
        pasta_destino = os.path.join(pasta_exe, "arquivos")

        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        # Processamento das páginas
        primeira_feita = False
        paginas_desde_salto = 0

        for i in range(total_paginas):
            writer.add_page(reader.pages[i])
            atual = i + 1
            if atual >= inicio:
                if not primeira_feita:
                    writer.add_blank_page()
                    primeira_feita = True
                else:
                    paginas_desde_salto += 1
                    if paginas_desde_salto == intervalo:
                        writer.add_blank_page()
                        paginas_desde_salto = 0

        # Define o nome final e salva na pasta local
        nome_original = os.path.basename(caminho_arquivo)
        caminho_saida = os.path.join(pasta_destino, f"PRONTO_{nome_original}")

        with open(caminho_saida, "wb") as f:
            writer.write(f)
            
        print(f"\n✅ SUCESSO!")
        print(f"📂 Arquivo salvo em: {caminho_saida}")

    except Exception as e:
        print(f"\n❌ ERRO: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        processar_pdf(sys.argv[1])
    else:
        arq = input("Arraste o PDF aqui e aperte Enter: ")
        if arq:
            processar_pdf(arq)
    input("\n--- Pressione Enter para fechar ---")