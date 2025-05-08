import time
import csv
from scholarly import scholarly

def buscar_artigos(termos_busca):
    artigos = []
    
    for termo in termos_busca:
        print(f"Buscando artigos para o termo: {termo}")
        
        # Buscar artigos no Google Scholar
        search_query = scholarly.search_pubs(termo)
        
        # Limitar a busca aos 100 primeiros artigos mais citados desde 2010
        count = 0
        while count < 100:
            try:
                artigo = next(search_query)
                
                # Verificar se o ano do artigo é maior ou igual a 2010
                if(artigo['bib']['pub_year'] == 'NA'):
                    continue
                if int(artigo['bib']['pub_year']) >= 2010:
                    # Coletar informações do artigo
                    artigo_info = {
                        'titulo': artigo['bib']['title'],
                        'ano': artigo['bib']['pub_year'],
                        'citacoes': artigo['num_citations'],
                        'revista': artigo['bib'].get('venue', 'N/A'),
                        'abstract': artigo['bib'].get('abstract', 'N/A')
                    }
                    artigos.append(artigo_info)
                    print(f"Artigo encontrado: {artigo_info['titulo']} ({artigo_info['ano']}) - Citado {artigo_info['citacoes']} vezes.")
                    count += 1
                else:
                    continue
            except StopIteration:
                break
        
            # Pausar para não fazer muitas requisições consecutivas (previne bloqueios)
            time.sleep(2)
    
    return artigos


def salvar_artigos_em_csv(artigos, arquivo_saida):
    # Definir os campos do CSV
    campos = ['titulo', 'ano', 'citacoes', 'revista', 'abstract']
    
    # Escrever os artigos no arquivo CSV
    with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        
        # Escrever o cabeçalho
        writer.writeheader()
        
        # Escrever os dados dos artigos
        for artigo in artigos:
            writer.writerow(artigo)
    
    print(f"Artigos salvos em {arquivo_saida}.")


def carregar_tags_do_arquivo(arquivo_entrada):
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        termos_busca = [linha.strip() for linha in f.readlines()]
    return termos_busca


if __name__ == "__main__":
    # Defina os arquivos de entrada e saída
    arquivo_entrada = "tags.txt"  # arquivo com as tags
    arquivo_saida = "resultados_artigos.csv"  # onde os resultados serão salvos em CSV
    
    # Carregar tags
    termos_busca = carregar_tags_do_arquivo(arquivo_entrada)
    
    # Buscar artigos
    artigos = buscar_artigos(termos_busca)
    
    # Salvar os artigos encontrados no arquivo CSV
    salvar_artigos_em_csv(artigos, arquivo_saida)
    
    print(f"Busca concluída. Os artigos foram salvos em {arquivo_saida}.")
