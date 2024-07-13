import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def extrair_informacoes_livro(url):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f'Falha ao acessar a página: {response.status_code}')
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    produtos = soup.find_all('div', class_='product-thumb')

    dados = []

    for produto in produtos:
        titulo_tag = produto.find('h4')
        titulo = titulo_tag.get_text(strip=True) if titulo_tag else "N/A"
        
        link_tag = titulo_tag.find('a') if titulo_tag else None
        link = link_tag['href'] if link_tag else "N/A"
        
        preco_old_tag = produto.find('span', class_='price-old')
        preco_old = preco_old_tag.get_text(strip=True) if preco_old_tag else "N/A"
        
        preco_new_tag = produto.find('span', class_='price-new')
        preco_new = preco_new_tag.get_text(strip=True) if preco_new_tag else "N/A"

        dados.append({
            'titulo': titulo,
            'preco_old': preco_old,
            'preco_new': preco_new,
            'link': link
        })

    return dados

# URL base da pesquisa
url_base = 'https://leitura.com.br/index.php?route=product/special&limit=96&page={}'

# Lista para armazenar todos os dados de todos os livros
todos_dados_livros = []

# Número máximo de páginas para iterar (exemplo: 5 páginas)
numero_de_paginas = 5

for pagina in range(1, numero_de_paginas + 1):
    url_pesquisa = url_base.format(pagina)
    
    # Extrair as informações dos produtos na página de pesquisa atual
    dados_livros = extrair_informacoes_livro(url_pesquisa)
    
    # Adicionar os dados extraídos da página atual à lista geral
    todos_dados_livros.extend(dados_livros)
    
    # Aguardar um tempo aleatório entre 1 e 3 segundos para evitar bloqueios
    time.sleep(random.randint(1, 3))

# Verificar se foram extraídos dados
if todos_dados_livros:
    # Converter os dados em um DataFrame pandas e salvar em um arquivo CSV
    df = pd.DataFrame(todos_dados_livros)
    df.to_csv('livros_leitura_todas_paginas.csv', index=False, encoding='utf-8')
    print("Dados salvos com sucesso em livros_leitura_todas_paginas.csv")
else:
    print("Nenhum dado foi extraído.")
