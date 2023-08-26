from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup

class Webscraping:
    
    #Selenium
    def __init__(self):
        self.servico = Service(ChromeDriverManager().install())
        self.navegador = webdriver.Chrome(service=self.servico)
          
    #Selenium
    def buscar_produto(self,produto):
        self.navegador.get("https://www.mercadolivre.com.br")
        caixaTexto = self.navegador.find_element(By.XPATH, '/html/body/header/div/div[2]/form/input')
        caixaTexto.send_keys(produto)
        caixaTexto.send_keys(Keys.ENTER)  
    
    #BeautifulSoup
    def pegar_codigo_fonte(self):
        self.site = BeautifulSoup(self.navegador.page_source,'html.parser')
        print(f'Titulo da pagina : {self.site.title.string}')
        return self.site
        
    #Beautifulsoup
    def lista_produtos(self,codigo_fonte):
        #Pegando a lista do resultado
        produtos = codigo_fonte.findAll('li', attrs={'class':'ui-search-layout__item'})
        return produtos
    
    #BeautifulSoup
    def produto(self,produtos):
        for produto in produtos:
            #attrs informa que o atributo a ser procurado sera class
            titulo = produto.find('h2',attrs={'class':'ui-search-item__title shops__item-title'})
            print(f'Titulo do anuncio : {titulo.text}')
            
            link = produto.find('a',attrs={'class':'ui-search-link'})
            print('Link : ',link['href'])

            real = produto.find('span', attrs={'class':'andes-visually-hidden'})
            centavos = produto.find('span', attrs={'class':'price-tag-cents'})
            if(centavos!=None):
                print(f'Preço :R$ {real.text},{centavos.text}')
            else:
                print(f'Preço :R$ {real.text}')
        
            frete = produto.find('span', attrs={'class':'ui-pb-highlight'})
            if(frete!=None):
                print(f'Frete: R$ {frete.text}')
            else:
                print('')
            

            
if __name__=='__main__':
    app = Webscraping()
    app.buscar_produto('ps5')
    sleep(1)
    codigo_fonte = app.pegar_codigo_fonte()
    produtos = app.lista_produtos(codigo_fonte)
    app.produto(produtos)
    
