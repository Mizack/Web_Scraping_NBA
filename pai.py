from selenium import webdriver

class Acessar_web:
    def __init__(self,url):
        navegador = webdriver.Firefox()
        self.navegador = navegador
        navegador.get(url)