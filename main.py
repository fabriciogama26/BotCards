from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import options
from selenium.webdriver.firefox.options import Options
import os
from time import sleep
import requests
from listtext import list


class BotCards:
    
    def __init__(self):

        global options

        global navegador

        global url

        global namecards

        namecards = []

        options = Options()
        options.headless = True
       
        navegador = webdriver.Firefox(options = options)

        url = "https://scryfall.com/search?as=full&order=name&q=set%3Abro&unique=cards"
        #url = "https://scryfall.com/search?q=set%3Admr&order=name&as=full&unique=prints"

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
            navegador.get(url)
            BotCards.CheckList(self)
            BotCards.ContPag(self)
            BotCards.ScrapWeb(self)
            BotCards.NumPag(self)
            BotCards.DataBase(self)
            
        except ValueError:

            sleep(60)
            navegador.quit()
            BotCards.Conexao(self)

    def ScrapWeb(self):   

        global namecard 

        sleep(3)

        try:

            for i in navegador.find_elements(by=By.CLASS_NAME,value="card-profile"):

                texto = i.find_element(by=By.CLASS_NAME,value="card-text-oracle").text

                namecard = i.find_element(by=By.CLASS_NAME,value="card-text-card-name").text

                BotCards.CheckDados(self)
                    
                for frase in list:
                    if frase in texto:

                        namecards.append(namecard)

                        img = i.find_element(by=By.CLASS_NAME,value="card-image-front")

                        img.screenshot("image.png")

                        break

                
        except ValueError:

            navegador.quit()
            BotCards.ScrapWeb(self)

    def CheckList(self):
        
        if not os.path.exists("cardslist.txt"):

            with open("cardslist.txt", "w") as dados:
                dados.close()

    def CheckDados(self):

        if not os.stat("cardslist.txt").st_size == 0:

            with open("cardslist.txt") as dados:

                cd = dados.readlines()
                
                for card in cd:
                    
                    if str(card).strip() == namecard:
                        break
                    break
                

    def NumPag(self):

        if float(numpag) > 1:

            pags = round(numpag)

            if pags <= 2:

                navegador.get("https://scryfall.com/search?as=full&order=name&page=2&q=set%3Admr&unique=prints")

                BotCards.ScrapWeb(self)

            else:

                for x in range(2,(int(pags)+1)):

                    navegador.get("https://scryfall.com/search?as=full&order=name&page="f'{x}'"&q=set%3Abro&unique=cards")
                    #navegador.get("https://scryfall.com/search?as=full&order=name&page="f'{x}'"&q=set%3Admr&unique=prints")

                    BotCards.ScrapWeb(self)

    def ContPag(self):

        sleep(3)

        TotalPag = navegador.find_element(by=By.XPATH,value="//*[@id='main']/div[2]/p/strong")

        la = TotalPag.text

        text2,text3,text4,text5,nuncards,text = la.split(" ")

        global numpag

        numpag = float(nuncards)/20

    def DataBase(self):

        with open("cardslist.txt", 'w') as cl:
            for x in namecards:
                cl.write(str(x))
                cl.write('\n')
            cl.close()


if __name__== '__main__':
    BotCards()