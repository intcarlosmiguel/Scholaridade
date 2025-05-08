from playwright.sync_api import sync_playwright
import requests
# Inicia o Playwright
with sync_playwright() as p:
    # Cria um navegador
    browser = p.chromium.launch(headless=False)  # headless=False para visualizar a execução
    page = browser.new_page()

    # Navega até o site do Google
    page.goto("https://sci-hub.se/")

    # Espera alguns segundos para que a página seja carregada (opcional)
    page.wait_for_timeout(100)  # espera 5 segundos
    #
    xpath = '//*[@id="request"]'  # XPath do campo de pesquisa no Google
    page.fill(xpath, "A new algorithm for achieving proportionality in user equilibrium traffic assignment")  # Digita o texto

    # Pressiona Enter
    page.press(xpath, "Enter")
    page.wait_for_timeout(5000)  
    pdf_url = page.query_selector('embed[type="application/pdf"]').get_attribute('src')
    print(f"Link do PDF: {pdf_url}") #
    pdf_url = "https://sci-hub.se" + pdf_url
    # Verifica se o PDF foi encontrado
    # Realiza o download do PDF
    if pdf_url:
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open("downloaded_file.pdf", "wb") as f:
                f.write(response.content)
            print("PDF baixado com sucesso!")
        else:
            print(f"Erro ao baixar o PDF. Status code: {response.status_code}") 
    browser.close()
