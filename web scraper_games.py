#Biblioteca Request que fará requisiçoes HTTP de forma facilitada
#Biblioteca BeautifulSoup para analisar documentos do HTML localizar dados e titulos
import requests
from bs4 import BeautifulSoup
import csv

url = 'https://br.ign.com/'
response = requests.get(url)
# Condição para verificar se a requisição request na pagina deu certo
if response.status_code == 200:
    conteudo_url = response.content
else:
    print(f'Falha ao acessar a página: {response.status_code}')

#html.parser que uma ferramenta dentro do python que que irá interpreta o conteudo HTML
soup = BeautifulSoup(response.content, 'html.parser')

#Variavel que irá encontra onde esta os artigos. No caso do Ign esta dentro de uma diva de classe tbl
artigos = soup.find_all('div', class_='tbl')

#Lista para armazenar os dados dos artigos de reviwe
dados = []
#article é um objeto dentro da biblioteca Beautiful irá fazer a bsuca de titulos,datas e links do site
for article in artigos:
    titulo = article.find('h3').get_text()
    data = article.find('time')
    link = article.find('a')['href']

#data.append({...}): Cria um dicionário com as chaves 'title', 'date' e 'link'
#Cada iteração do loop for article in articles extrai informações de um artigo específico
#  e adiciona essas informações como um novo dicionário à lista data.
    data.append({
        'titulo': titulo,
        'data': data,
        'link': link
    })

with open('atigos.csv', mode='w' , newline='',encodin='utf-8') as file:
    dados_site = csv.DictWriter(file, fieldnames=['titulo' , 'data' , 'link'])
    dados_site.writeheader()
    for dado in data:
        dados_site.writerow(dado)


print('Dados salvos com sucesso em artigos.csv')


