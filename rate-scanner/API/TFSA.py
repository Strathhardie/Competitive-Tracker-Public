import json
import re

import requests
from bs4 import BeautifulSoup
from autoscraper import AutoScraper

def td_tfsa(): 
    url = 'https://www.td.com/ca/en/personal-banking/products/bank-accounts/account-rates/'

    # We can add one or multiple candidates here.
    # You can also put urls here to retrieve urls.
    wanted_list = ["0.010%"]

    scraper = AutoScraper()
    result = scraper.build(url, wanted_list)
    return(result[1])

def bmo_tfsa(): 
    url = 'https://www.bmo.com/main/personal/investments/rates/'
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    print(soup)

def scotia_tfsa(): 
    url = 'https://www.scotiabank.com/ca/en/personal/rates-prices/savings-account-rates.html'

    # We can add one or multiple candidates here.
    # You can also put urls here to retrieve urls.
    wanted_list = ["0.010%"]

    scraper = AutoScraper()
    result = scraper.build(url, wanted_list)
    return(result)

def hsbc_tfsa(): 
    url = "https://www.hsbc.ca/bank-with-us/todays-rates/#registered-plan"

def nbc_tfsa(): 
    url = "https://www.nbc.ca/personal/savings-investments/accounts/cash-advantage.html"

def simplii_tfsa():
    url = "https://www.simplii.com/en/rates/tfsa-rates.html"

def eq_tfsa(): 
    url = "https://www.eqbank.ca/personal-banking/tfsa"

def motus_tfsa(): 
    url = "https://www.motusbank.ca/Support/Rates"

def duca_tfsa(): 
    url = "https://www.motusbank.ca/Support/Rates"

def meridian_tfsa(): 
    url = "https://www.meridiancu.ca/Personal/Meridian-Rates-Fees.aspx"

def motive_tfsa(): 
    url = "https://www.motivefinancial.com/Rates/"

def manulife_tfsa(): 
    url = "https://www.manulifebank.ca/personal-banking/investments/tax-free-savings-account.html"


print(td_tfsa())