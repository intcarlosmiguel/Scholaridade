from playwright.sync_api import sync_playwright
import requests
import pandas as pd
from tqdm import tqdm
import os
# Inicia o Playwright

artigos = pd.read_csv("./output/resultados_artigos.csv")

# Verifica se a pasta "artigos" existe, caso contrário, cria a pasta
if not os.path.exists("artigos"):
    os.makedirs("artigos")

lista = []
link = "https://sci-hub.se/"
with sync_playwright() as p:
    # Cria um navegador
    
    browser = p.chromium.launch(headless=False)  # headless=False para visualizar a execução
    page = browser.new_page()
    for titulo in tqdm(artigos["titulo"].values):
        # Navega até o site do Google   
        page.goto(link)

        # Espera alguns segundos para que a página seja carregada (opcional)
        page.wait_for_timeout(100)  # espera 5 segundos
        #
        xpath = '//*[@id="request"]'  # XPath do campo de pesquisa no Google
        page.fill(xpath, titulo)  # Digita o texto

        # Pressiona Enter
        page.press(xpath, "Enter")
        page.wait_for_timeout(5000)
        try:
            pdf_url = page.query_selector('embed[type="application/pdf"]').get_attribute('src')
            pdf_url = link + pdf_url
            # Verifica se o PDF foi encontrado
            # Realiza o download do PDF
            titulo = titulo.replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_").replace("?", "_")
            titulo = titulo.replace(";", "_").replace(",", "_").replace("'", "_").replace('"', "_")
            titulo = titulo.lower()
            if pdf_url:
                response = requests.get(pdf_url)
                if response.status_code == 200:
                    with open(f"./artigos/{titulo}.pdf", "wb") as f:
                        f.write(response.content)
                    size += 1
                else:
                    print(f"Erro ao baixar o PDF. Status code: {response.status_code}")
        except Exception as e:
            lista.append(titulo)
    
    if not os.path.exists("falied_artigos"):
        os.makedirs("falied_artigos")
    # Salva os títulos que falharam em um arquivo txt
    with open("falied_artigos/falied_artigos.txt", "w") as f:
        for item in lista:
            f.write("%s\n" % item)
    
    
    browser.close()
