from yaml_utils import YAMLUtils
from bs4 import BeautifulSoup as b
import requests
import json
from datetime import datetime
from selenium import webdriver


def get_special_offers():
    banks = YAMLUtils.readYAML(YAMLUtils.FILE_NAME)

    try:
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = True
        driver = webdriver.Firefox(options=fireFoxOptions)

        special_offers_dictionary = {}
        for index, bank in enumerate(banks):
            special_offers_dictionary[index] = {}

            special_offers_dictionary[index]['institution_name'] = bank['name']

            for account in bank['accounts']:
                driver.get(account['url'])
                soup = b(driver.page_source,'html5lib')
                
                special_offers_dictionary[index]['accounts'] = []

                account_dictionary = {}
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