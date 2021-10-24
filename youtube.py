from selenium import webdriver
from bs4 import BeautifulSoup
from pai import Acessar_web
import time
url = 'https://www.youtube.com/channel/UCYfdidRxbB8Qhf0Nx7ioOYw'

class Youtube(Acessar_web):
    def __init__(self,url):
        # acessando superclasse
        super().__init__(url)
        # instanciando navgador
        nav = self.navegador
        self.nav = nav
        

    def acessar_codigo_html(self):
        # idicando local em que os vídeos se encontram
        videos = self.nav.find_element_by_xpath('//*[@id="dismissible"]')
        # clicando na seta para pegar todos os vídeos selecionados
        self.nav.find_element_by_xpath('//*[@id="right-arrow"]/ytd-button-renderer').click()
        # salvando dados da pagina
        html = videos.get_attribute('outerHTML')
        # fechando wd
        self.nav.quit()
        return html

    def separar_dados(self):
        # parseando dados
        soup = BeautifulSoup(self.acessar_codigo_html(),'html.parser')
        titulos_pg = soup.find(name='span',attrs={'id':'title'})
        titulos = soup.find_all(name='a',attrs={'id':'video-title'})
        canais = soup.find_all(name='a',attrs={'class':'yt-simple-endpoint style-scope yt-formatted-string'})
        data_postages_views = soup.find_all(name='span',attrs={'class':'style-scope ytd-grid-video-renderer'})
        tempo_videos = soup.find_all(name='span',attrs={'id':'text'})
        links = soup.find_all(name='a',attrs={'id':'thumbnail'})

    def data_agora(self):
        pass




# aaa = Youtube(url).separar_dados()


# instanciando navegador
# navegador = webdriver.Firefox()
# navegador.get(url)
# # selecionando dados
# videos = navegador.find_element_by_xpath('//*[@id="dismissible"]')
# navegador.find_element_by_xpath('//*[@id="right-arrow"]/ytd-button-renderer').click()
# html = videos.get_attribute('outerHTML')
# # fechando navegador
# navegador.quit()

# soup = BeautifulSoup(html,'html.parser')
# tempo_videos = soup.find_all(attrs={'class':'style-scope ytd-thumbnail-overlay-time-status-renderer','class':'style-scope ytd-thumbnail-overlay-time-status-renderer','class':'style-scope ytd-thumbnail-overlay-time-status-renderer'})#,attrs={'class':'style-scope ytd-thumbnail-overlay-time-status-renderer'})

# titulo_pg = soup.find(name='span',attrs={'id':'title'})
# titulos = soup.find_all(name='a',attrs={'id':'video-title'})
# kenells = soup.find_all(name='a',attrs={'class':'yt-simple-endpoint style-scope yt-formatted-string'})
# data_postages_views = soup.find_all(name='span',attrs={'class':'style-scope ytd-grid-video-renderer'})
# links = soup.find_all(name='a',attrs={'id':'thumbnail'})

# contagem = 0
# for sea in data_postages_views:
    
#     teste = sea.text.strip()
#     if contagem%2 != 0:
#         print(contagem,'\t',teste,'\n\n\n')
#     # else:
#     #     print(contagem,'\t',teste,'\n\n\n')
#     contagem += 1
# print(contagem)

# contagem2 = 0
# for kenell2 in links:
#     kenell3 = kenell2.get('href')
#     print(contagem2,'\t',kenell3,'\n\n\n')
#     contagem2 += 1
# print(contagem2)
# print(titulo_pg)

# contagem2 = 0
# for kenell2 in tempo_videos:
#     kenell3 = kenell2.text.strip()
#     print(contagem2,'\t',kenell3,'\n\n\n')
#     contagem2 += 1
# print(tempo_videos)