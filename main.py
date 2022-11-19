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

        url = "https://scryfall.com/sets/bro?as=text&order=name"

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

            listcards = navegador.find_elements(by=By.PARTIAL_LINK_TEXT,value=list)

            for i in listcards:
                print(str(i.text))
                with open("element.png", "wb") as elem_file:
                    elem_file.write(i.screenshot_as_base64)
                    elem_file.close()


                
        except ValueError:

            navegador.quit()
            BotCards.ScrapWeb(self)

if __name__== '__main__':
    BotCards()