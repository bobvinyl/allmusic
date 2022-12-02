from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

class allmusic_disco_scraper:
    
    options = Options()
    options.headless = True
    options.add_argument("--window-size=640,480")

    driver_path = '../chrome/chromedriver.exe'
    driver = None
    
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        
    def __del__(self):
        self.driver.quit()
        
    def __get_score(self,match_obj):
        if match_obj.group(1) is not None:
            return match_obj.group(1)
    
    def __fixRating(self,html):        
        reg = r'\<span class="allmusic-rating rating-allmusic-([0-9]{1}).*\</span\>'
        html = re.sub(reg, self.__get_score, html)
        
        reg = r'\<span class="average-user-rating rating-average-([0-9]{2}).*\</span\>'
        html = re.sub(reg, self.__get_score, html)
        
        return html
    
    def disco_to_dataframe(self,artist,artist_url):
        artist_url = artist_url + '/discography'
        self.driver.get(artist_url)
        html = self.driver.page_source

        # Parse via BS4
        soup = BeautifulSoup(html, "html.parser")
        disco = soup.find_all('table')[0]
        disco = self.__fixRating(str(disco))

        df = pd.read_html(disco)[0]
        df['Artist'] = artist
        #df['User Hold'] = df['User Ratings']
        print(df['User Ratings'])
        df['User Rating'] = pd.to_numeric(df['User Ratings'].str[0:2]).apply(lambda x: np.nan if x==0 else x) # Fix this to allow for no user reviews
        df['User Count'] = pd.to_numeric(df['User Ratings'].str[4:-1].replace(',','', regex=True))
        df['AllMusic Rating'] = df['AllMusic Rating'] + 1
        df = df.loc[:,['Artist','Year','Album','Label','AllMusic Rating','User Rating','User Count']]
        
        return df