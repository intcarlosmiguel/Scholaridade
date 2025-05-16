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
lista_pdf = []
link = "https://sci-hub.se/"
with sync_playwright() as p:
    # Cria um navegador
    
    browser = p.chromium.launch(headless=False)  # headless=False para visualizar a execução
    page = browser.new_page()
    for titulo in tqdm(artigos["titulo"].values):
        # Navega até o site do Google   
        page.goto(link)

        # Espera alguns segundos para que a página seja carregada (opcional)
        page.wait_for_timeout(1000)  # espera 5 segundos
        #
        xpath = '//*[@id="request"]'  # XPath do campo de pesquisa no Google


        # Pressiona Enter
        page.press(xpath, "Enter")
        page.wait_for_timeout(1000)
        xpath = '//*[@id="pdf"]'  # XPath do botão de pesquisa
        try:
            pdf_url = page.query_selector('embed[type="application/pdf"]').get_attribute('src')
            #print("Url inicial: ",pdf_url)
            if not pdf_url.startswith('//2024.sci-hub.se'):
                if not pdf_url.startswith('//dacemirror'):
                    if not pdf_url.startswith('http'):
                        pdf_url = link + pdf_url.lstrip('/')
                else:
                    pdf_url = pdf_url.replace("//dacemirror", "dacemirror")
            else:
                pdf_url = pdf_url.replace("//2024.sci-hub.se", "2024.sci-hub.se")
            #print("Url final: ",pdf_url)
            # Ensure the URL has the correct protocol
            if pdf_url.startswith("2024.sci-hub.se"):
                pdf_url = "https://" + pdf_url
            elif pdf_url.startswith("dacemirror"):
                pdf_url = "https://" + pdf_url
            elif pdf_url.startswith("//"):
                pdf_url = "https:" + pdf_url
            # Download the PDF directly using requests
            response = requests.get(pdf_url)
            titulo_limpo = titulo.replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_").replace("?", "_")
            titulo_limpo = titulo_limpo.replace(";", "_").replace(",", "_").replace("'", "_").replace('"', "_").lower()
            with open(f"artigos/{titulo_limpo}.pdf", "wb") as f:
                f.write(response.content)
        except Exception as e:
            lista.append(titulo)
        
    if not os.path.exists("falied_artigos"):
        os.makedirs("falied_artigos")
    # Salva os títulos que falharam em um arquivo txt
    with open("falied_artigos/falied_artigos.txt", "w") as f:
        for item in lista:
            f.write("%s\n" % item)
    browser.close()
