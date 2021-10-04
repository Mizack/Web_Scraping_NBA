from os import replace
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

# pegar o conteudo html a partir da url
url = 'https://www.mercadolivre.com.br/ofertas#c_id=/home/promotions-recommendations/element&c_uid=21f4deef-3a15-4753-9c18-9b08f5654778'

# instanciar navegador
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'.\geckodriver.exe')
driver.get(url)

# indicando xpath
produtos = driver.find_element_by_xpath('//*[@id="root-app"]/div/section[2]/div/div[2]/div/ol')
html_salvo = produtos.get_attribute('outerHTML')

# fechando navegador
driver.quit()

# salvando html e separando informações
sopu = BeautifulSoup(html_salvo,'html.parser')
valores = sopu.find_all(name='span',attrs={'class':'promotion-item__price'})
links = sopu.find_all(name='a',attrs={'class':'promotion-item__link-container'})
titulos = sopu.find_all(name='p',attrs={'class':'promotion-item__title'})

# ajustando a descrição e salvando em uma lista
titulo_lista = []
for titulo in titulos:
    descricao = titulo.text.strip()
    titulo_lista.append(descricao)

# ajustando o link e salvando em uma lista
link_lista = []
for link in links:
    caminho = link.get('href')
    link_lista.append(caminho)

# ajustando o valor e salvando em uma lista
valor_lista = []
for valor in valores:
    # verificando se é um valor decimal
    try:
        centavo = valor.sup.text
    except:
    # caso seja inteiro, retorna um 0
        centavo = '00'
    valor_final = valor.span.text+','+centavo
    valor_final = valor_final.replace('R$ ','').replace('.','').replace(',','.')
    valor_lista.append(float(valor_final))

# adicionando listas em um dataframe
dados = pd.DataFrame({'produto':titulo_lista,'valor':valor_lista,'link':link_lista})
dados['index'] = dados.index
print(dados)

# gerando JSON
produtos_json = {}
produtos_json['prod_json'] = dados.to_dict('records')
arq_ = json.dumps(produtos_json,ensure_ascii=False)
arq_final = open('ranking2.json','w',encoding="utf8")
arq_final.write(arq_)
arq_final.close()