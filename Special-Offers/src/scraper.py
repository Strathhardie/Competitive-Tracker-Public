from yaml_utils import YAMLUtils
from bs4 import BeautifulSoup as b
import requests
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import chromedriver_binary  # Adds chromedriver binary to path
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import pandas as pd

"""
Makes various requests to bank websites and returns a dictionary containing special offers.

Args: 
    None

Returns:
    dict: a dict with keys of financial institutions and values representing special offers.
"""



"""
Makes various requests to bank websites and returns a dictionary containing special offers.

Args: 
    None

Returns:
    dict: a dict with keys of financial institutions and values representing special offers.
"""


def get_special_offer_accounts():
    #reading YAML File
    banks = YAMLUtils.readYAML("../"+YAMLUtils.FILE_NAME)

    # Create a progress bar
    t = tqdm(banks, desc="Auditing Changes", leave=True, ncols=100, position=0)

    try:
        #Selenium Driver initialization 
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = True
        # driver = webdriver.Firefox(options=fireFoxOptions)

        # This is for google chrome
        driver = webdriver.Chrome(ChromeDriverManager().install())


        special_offers_dictionary = {}
        for index, bank in enumerate(banks):
            t.set_description("%-15s" % str(bank['name']))
            t.update()

            special_offers_dictionary[index] = {}

            special_offers_dictionary[index]['institution_name'] = bank['name']

            special_offers_dictionary[index]['accounts'] = []


            for account in bank['accounts']:
                driver.get(account['url'])

                soup = b(driver.page_source,'html5lib')
                
                account_dictionary = {}
                account_dictionary['account_url']=account['url']
                account_dictionary['account_category'] = account['account_category']
                for k,v in account['elements'].items():                       
                    account_dictionary[k] = [x.text.strip() for x in soup.select(v)]
                special_offers_dictionary[index]['accounts'].append(account_dictionary)
    finally:
        try:
            driver.quit()
        except:
            pass
    
    return special_offers_dictionary


def main():
    print("Running..")
    df = pd.DataFrame(data=get_special_offer_accounts(), index=[0])
    print(df.head())
    df.to_excel('dictionary.xlsx')
main()
