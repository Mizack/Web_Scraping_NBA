import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

# pegar o conteudo html a partir da url
url = 'https://www.nba.com/stats/players/boxscores-traditional/'

# instanciar navegador
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'.\geckodriver.exe')
driver.get(url)
time.sleep(10)
try:
    verifica = True
    while verifica:
        try:
            # fechar cookie
            # time.sleep(10)    
            driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
            print('fechou cookie')
            verifica = False
        except:
            print('cookie nao apareceu')
    # clicando no filtro
    time.sleep(20)
    driver.find_element_by_xpath('/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/thead/tr/th[8]').click()
    print('clicou no filtro')
    # salvar elemento html
    time.sleep(1)
    elemento = driver.find_element_by_xpath('/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table')
    # salvar conteudo
    time.sleep(1)
    html_salvo = elemento.get_attribute('outerHTML')
    print(html_salvo)

except:
    print("Deu ruim na captação de dados")

try:
    # parsear o html 
    sopu = BeautifulSoup(html_salvo,'html.parser')
    tabela = sopu.find(name='table')
    # print(tabela)
    print('passou na primeira etapa de limpar os dados')

    # estruturar conteudo em um dataframe
    dados = pd.read_html(str(tabela))[0].head(10)
    print('recebeu dados 1')
    print(dados.columns)
    dados['index1'] = dados.index

    df = dados[['index1','Player','Team','PTS']]
    print('recebeu dados 2')

    # df.columns = ['Player','Team','PTS']
    print(df)
    print('recebeu dados 3')
except:
    print('deu ruim na limpeza dos dados')
driver.quit()
try:
    # transformando em json
    top10 = {}
    top10['points'] = df.to_dict('records')
    print(top10['points'])
    arq_ = json.dumps(top10)
    arq_final = open('ranking2.json','w')
    arq_final.write(arq_)
    arq_final.close()
except:
    print('json deu pau')