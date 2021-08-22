import json
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from autoscraper import AutoScraper


def bmo_rrsp():
    url = 'https://www.bmo.com/bmocda/templates/json_rrsp_include.jsp'
    response = requests.request("GET", url)
    start_index = response.text.find("value") + 8
    offer = response.text[start_index:start_index + 6] + "%"
    return offer


def scotia_rrsp():
    url = 'https://www.scotiabank.com/ca/en/personal/rates-prices/resp-rrsp-rrif-rates.html'
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all("td")
    return "0.010%"


def hsbc_rrsp():
    url = "https://www.hsbc.ca/bank-with-us/todays-rates/#registered-plan"
    wanted_list = ["0.01%"]

    scraper = AutoScraper()
    result = scraper.build(url, wanted_list)
    return (result[5])

def nbc_rrsp():
    url = "view-source:https://www.nbc.ca/personal/savings-investments/accounts/cash-advantage.html"
    response = requests.request("GET", url)
    print(response.text)
    return "0.050%"

def simplii_rrsp():
    ## BS4 CAN NOT RETURN THE RATE AS IT IS RETRIEVED FROM RDBMS
    # url = "https://www.simplii.com/en/rates/tfsa-rates.html"
    # response = requests.request("GET", url)
    # soup = BeautifulSoup(response.text, features="html.parser")
    # offer = soup.find_all(class_="data-rds")
    return "0.10%"


def eq_rrsp():
    url = "https://www.eqbank.ca/personal-banking/rsp"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find("h3").text
    return offer[:45]


def motus_rrsp():
    url = "https://www.motusbank.ca/Support/Rates"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all("h5")[10].text
    return offer


def duca_rrsp():
    url = "https://www.duca.com/rates"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all("td")[24].text
    return offer


def meridian_rrsp():
    url = "https://www.meridiancu.ca/personal/rates-and-fees"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all("td")[5].text
    return offer


def motive_rrsp():
    url = "https://www.motivefinancial.com/Rates/"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all("td")[15].text[:6]
    return offer


def motive_rrsp2():
    url = "https://www.motivefinancial.com/Rates/"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all("td")[17].text[:6]
    return offer


def manulife_rrsp():
    url = "https://www.manulifebank.ca/personal-banking/investments/tax-free-savings-account.html"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all(class_="rates-fees__value")[1].text
    return offer


def merged_rrsp_rates():
    merged_rates = [bmo_rrsp(), scotia_rrsp(), hsbc_rrsp(), nbc_rrsp(), simplii_rrsp(), eq_rrsp(),
                    motus_rrsp(), duca_rrsp(), meridian_rrsp(), motive_rrsp(), motive_rrsp2(), manulife_rrsp()]
    result = list(map(lambda x: round(float(x.strip("%")), 2), merged_rates))
    return result


def merged_rrsp_names():
    return [ "BMO", "ScotiaBank", "HSBC", "NBC", "Simplii", "EQ", "Motus", "DUCA", "Meridian", "Motive",
            "Manulife"]

def rrsp_df():
    accounts = merged_rrsp_names()
    rates = merged_rrsp_rates()
    res = dict(zip(accounts, rates))

    df = pd.DataFrame(data=res, index=[0])

    return df

def main():
    rrsp_df().to_csv("rrsp_rates")


if __name__ == "__main__":
    main()
