from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import options
from selenium.webdriver.firefox.options import Options
from time import sleep
import requests
from listtext import list


class BotCards:
    

    def __init__(self):

        global options

        global navegador

        global url

        options = Options()
        options.headless = True
       
        navegador = webdriver.Firefox(options = options)

        url = "https://scryfall.com/search?as=full&order=name&q=set%3Abro&unique=prints"

        try:

            BotCards.Conexao(self)

        except ValueError:

            sleep(10)
            BotCards.__init__(self)
        
        finally:

            navegador.quit()
 

    def Conexao(self):
                  
        ''' checar conexão de internet '''
        
        timeout = 5
        try:
            requests.get(url, timeout=timeout)
            BotCards.ScrapWeb(self)
            
        except:
            sleep(60)
            BotCards.Conexao(self)

    def ScrapWeb(self):    

        navegador.get(url)

        sleep(1)

        try:

            for i in navegador.find_elements(by=By.CLASS_NAME,value="card-profile"):

                texto = i.find_element(by=By.CLASS_NAME,value="card-text-oracle").text

                for frase in list:
                    if frase in texto:

                        img = i.find_element(by=By.CLASS_NAME,value="card-image-front")

                        img.screenshot("image.png")

                        break
      
        except ValueError:

            navegador.quit()
            BotCards.ScrapWeb(self)

if __name__== '__main__':
    BotCards()