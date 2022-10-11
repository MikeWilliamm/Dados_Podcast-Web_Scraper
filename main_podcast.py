import requests
from bs4 import BeautifulSoup as bs #código hrml ficara mais legivel, encontrara elementos
import logging
import pandas as pd 
import os

#NoS prints acima, observase que nao trousse a lista completa de podcast, 
#isso acontece devido o site não carregar completo de uma só vez.

#Atraves do google inspect, na aba network, ao rolar a pagina para baixo, 
#para carregar mais elementos, é possivel visualizar a geranção do arquivo 'ajax=true'
# nele existe um link, esse link possui e numeração de páginas, 
# atraves dele pode-se acessar todas as páginas.
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

#URL original do site: 'https://portalcafebrasil.com.br/todos/podcasts/'
url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'


def get_podcast(url):
    retorno = requests.get(url)
    soup = bs(retorno.text)
    return soup.find_all('h5')

#automarizando a captura de dados de todas as paginas ---------------------------
contador = 0
lista_podcast = []
lista_aux = []

while True:
    contador += 1
    lista_aux = get_podcast(url.format(contador))
    log.debug(f'Coletado {len(lista_aux)} do link: {url.format(contador)}')
    if len(lista_aux) < 1:
        break
    lista_podcast = lista_podcast + lista_aux
    lista_aux.clear()



lista_podcast
df = pd.DataFrame(columns=['EP','Link'])


for item in lista_podcast:
    df.loc[df.shape[0]] = [item.text, item.a['href']] #df.shape[0] tras a qtd de linhas, ao em vez do df.shape[0], pode-se usar o len(df), mas o len(df) e mais lento

absFilePath = os.path.dirname(os.path.realpath(__file__))
arq = f'{absFilePath}\podcast.csv'
df.to_csv(arq, encoding='utf-8', index=False, sep=';')
print(f'Arquivo imoveis.csv Exportado!')



