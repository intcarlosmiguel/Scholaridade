import fitz  # PyMuPDF

# Caminho para o arquivo PDF
pdf_path = './artigos/10.1287@trsc.2018.0845.pdf'

# Abre o PDF
doc = fitz.open(pdf_path)

# Itera sobre as páginas e extrai o texto
for i, page in enumerate(doc):
    text = page.get_text()

    lines = text.split('\n')
    abstract_found = False
    abstract_text = []

    for line in lines:
        if not abstract_found and 'abstract' in line.lower():
            abstract_text.append(line)
            abstract_found = True
            continue

        if abstract_found:
            abstract_text.append(line)
            if line.endswith('.') and lines[lines.index(line) + 1][0].isupper():
                break

    if abstract_text:
        print('Abstract found:')
        print(' '.join(abstract_text))

doc.close()
