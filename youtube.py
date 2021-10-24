from selenium import webdriver
from bs4 import BeautifulSoup
from pai import Acessar_web
from datetime import datetime
import time
import pandas as pd
url = 'https://www.youtube.com/channel/UCYfdidRxbB8Qhf0Nx7ioOYw'
# url = 'https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ'
# identi = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse[4]/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[5]/div[3]/ytd-shelf-renderer/div[1]'
identi = '//*[@id="dismissible"]'
class Youtube(Acessar_web):
    def __init__(self,url):
        # acessando método da superclasse
        super().__init__(url)
        # instanciando navgador
        nav = self.navegador
        self.nav = nav
        

    def acessar_codigo_html(self,identificador):
        # idicando local em que os vídeos se encontram
        time.sleep(10)
        try:
            
            videos = self.nav.find_element_by_xpath(identificador)
            # clicando na seta para pegar todos os vídeos selecionados
            self.nav.find_element_by_xpath('//*[@id="right-arrow"]/ytd-button-renderer').click()
            # salvando dados da pagina
            html = videos.get_attribute('outerHTML')
            print(html)
            # fechando wd
            self.nav.quit()
            return html
        except:
            self.nav.quit()
            print('Falha na captura de dados')


    def separar_dados(self):
        # parseando dados
        soup = BeautifulSoup(self.acessar_codigo_html(identi),'html.parser')
        titulos_pg = soup.find(name='span',attrs={'id':'title'})
        titulos = soup.find_all(name='a',attrs={'id':'video-title'})
        print(titulos)
        canais = soup.find_all(name='a',attrs={'class':'yt-simple-endpoint style-scope yt-formatted-string'})
        data_postages_views = soup.find_all(name='span',attrs={'class':'style-scope ytd-grid-video-renderer'})
        links = soup.find_all(name='a',attrs={'id':'thumbnail'})
        return titulos_pg,titulos,canais,data_postages_views,links
        # tempo_videos = soup.find_all(name='span',attrs={'id':'text'})


    def extrair_dados_coletados(self,dados,link=None,separador=None):
        lista_dados = []
        visualizacoes =[]
        contagem = 0
        for dado in dados:

            # separador padrão
            if link == None and separador == None:
                valor = dado.text.strip()
                lista_dados.append(valor)
                
            # separador de link
            elif link != None and separador == None:
                valor = dado.get('href')
                lista_dados.append(valor)

            # separador visualização e tempo postagem
            elif link == None and separador != None:
                valor = dado.text.strip()
                # tempo postagem
                if contagem%2 != 0:
                    lista_dados.append(valor)
                # visualizações
                else:
                    visualizacoes.append(valor)
            contagem += 1

        # separador de retorno
        if link == None and separador != None:
            return lista_dados,visualizacoes
        else:
            return lista_dados


    def data_agora(self):
        return datetime.today()

    
    def gerar_csv(self):
        titulos_pg,titulos,canais,data_postages_views,links = self.separar_dados()
        title = self.extrair_dados_coletados(titulos_pg)
        name = self.extrair_dados_coletados(titulos)
        channel = self.extrair_dados_coletados(canais)
        time,view = self.extrair_dados_coletados(data_postages_views,None,'dados')
        link = self.extrair_dados_coletados(links,'dados')

        df = pd.DataFrame({'TITULO':name,'CANAL':channel,'TEMPO_POSTAGEM':time,'VISUALIZACOES':view,'LINK_VIDEO':link,'DATA_ACESSO':self.data_agora()})
        print(df)
        title_alt = str(title).replace('[','').replace(']','').replace("'","").replace('í','i').replace(' ','_')
        df.to_csv(str(title_alt+'.csv'),index=False,sep='\t')
        
        
    def ler_arq_final(self):
        dados = pd.read_csv('Novos_videos.csv',sep='\t')
        return dados


ytb = Youtube(url)
ytb.gerar_csv()


