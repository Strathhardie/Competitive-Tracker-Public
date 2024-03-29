import json
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from autoscraper import AutoScraper

def td_tfsa(): 
    url = 'https://www.td.com/ca/en/personal-banking/products/bank-accounts/account-rates/'

    # We can add one or multiple candidates here.
    # You can also put urls here to retrieve urls.
    wanted_list = ["0.050%"]

    scraper = AutoScraper()
    result = scraper.build(url, wanted_list)
    return(result[1])

def bmo_tfsa(): 
    url = 'https://www.bmo.com/bmocda/templates/json_gic_include.jsp'
    response = requests.request("GET", url)
    start_index = response.text.find("value") + 8
    offer = response.text[start_index:start_index+5] + "%"
    return offer


def scotia_tfsa(): 
    url = 'https://www.scotiabank.com/ca/en/personal/rates-prices/savings-account-rates.html'
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all("td")
    return "0.050%"


def hsbc_tfsa(): 
    ## Using AutoScraper b/c I'm lazy
    url = "https://www.hsbc.ca/bank-with-us/todays-rates/#registered-plan"
    wanted_list = ["0.00%"]

    scraper = AutoScraper()
    result = scraper.build(url, wanted_list)
    return(result[1])

def nbc_tfsa(): 
    
    url = "view-source:https://www.nbc.ca/personal/savings-investments/accounts/cash-advantage.html"
    response = requests.request("GET", url)
    #print(response.text)
    return "0.050%"


def simplii_tfsa():
    ## BS4 CAN NOT RETURN THE RATE AS IT IS RETRIEVED FROM RDBMS
    #url = "https://www.simplii.com/en/rates/tfsa-rates.html"
    #response = requests.request("GET", url)
    #soup = BeautifulSoup(response.text, features="html.parser")
    #offer = soup.find_all(class_="data-rds")
    return "0.10%"

def eq_tfsa(): 
    url = "https://www.eqbank.ca/personal-banking/tfsa"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find("h3").text
    return offer[:5]


def motus_tfsa(): 
    url = "https://www.motusbank.ca/Support/Rates"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all("h5")[7].text
    return offer

def duca_tfsa(): 
    url = "https://www.duca.com/rates"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all("td")[22].text
    return offer

def meridian_tfsa(): 
    url = "https://www.meridiancu.ca/Personal/Meridian-Rates-Fees.aspx"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all("td")[3].text
    return offer

def motive_tfsa(): 
    url = "https://www.motivefinancial.com/Rates/"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all("td")[13].text[:6]
    return offer

def manulife_tfsa(): 
    url = "https://www.manulifebank.ca/personal-banking/investments/tax-free-savings-account.html"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all(class_="rates-fees__value")[0].text
    return offer


def merged_tfsa_rates(): 
    merged_rates = [td_tfsa(), bmo_tfsa(), scotia_tfsa(), hsbc_tfsa(), nbc_tfsa(), simplii_tfsa(), eq_tfsa(), motus_tfsa(), duca_tfsa(), meridian_tfsa(), motive_tfsa(), manulife_tfsa()]
    result = list(map(lambda x: round(float(x.strip("%")), 2), merged_rates))
    return result

def merged_tfsa_names(): 
    return ["TD", "BMO", "ScotiaBank", "HSBC", "NBC", "Simplii", "EQ", "Motus", "DUCA", "Meridian", "Motive", "Manulife"]

def tfsa_df(): 
    accounts = merged_tfsa_names()
    rates = merged_tfsa_rates()
    res = dict(zip(accounts,rates))
    
    df = pd.DataFrame(data=res, index=[0])
    
    return df



def main():
    tfsa_df().to_csv("tfsa_rates")



if __name__ == "__main__":
    main()
