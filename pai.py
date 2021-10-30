from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class Acessar_web:
    def __init__(self,url):
        options = Options()
        options.headless = True
        navegador = webdriver.Firefox(options=options)
        self.navegador = navegador
        navegador.get(url)