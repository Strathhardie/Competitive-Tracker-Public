import requests
from bs4 import BeautifulSoup
import pandas as pd
from autoscraper import AutoScraper

def rbc_rrsp():
    # Needs Refactoring
    
    url = 'https://www.rbcroyalbank.com/rates/rsp.html'

   
    wanted_list = ["0.050%"]

    scraper = AutoScraper()
    result = scraper.build(url, wanted_list)
    return (result[1])


def scotia_rrsp():
    ## Rendered using JS, Colin to look at? 
    url = 'https://www.scotiabank.com/ca/en/personal/rates-prices/resp-rrsp-rrif-rates.html'
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    print(soup)

    return "0.01%"


def nbc_rrsp():
    # BS4 Can not find elements in the rendered table - someone else to attempt?

    url = "https://www.nbc.ca/personal/savings-investments/accounts/cash-advantage.html"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    print(soup)

    return "0.05%"


def motus_rrsp():
   # todo
    url = "https://www.motusbank.ca/Support/Rates"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    return "1.00%"


def meridian_rrsp():
    #todo
    
    url = "https://www.meridiancu.ca/Personal/Meridian-Rates-Fees.aspx"
    #response = requests.request("GET", url)
    #soup = BeautifulSoup(response.text, features="html.parser")
    #offer = soup.find_all("td")[5].text

    offer = "0.01%"
    return offer


def motive_rrsp():
    url = "https://www.motivefinancial.com/Rates/"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all("td")[1].text[:6]
    return offer


def manulife_rrsp():
    # Todo
    
    url = "https://www.manulifebank.ca/personal-banking/investments/rrsp.html#rates"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    offer = soup.find_all(class_="rates-fees__value")[0].text

    return print(offer)

def td_rrsp(): 
    # Todo
    return "0.01%"

def hsbc_rrsp(): 
    # Todo
    
    return "0.01%"

def simplii_rrsp(): 
    # Todo
    return "0.01%"


def eq_rrsp(): 
    # Todo 
    return "0.01%"

def bmo_rrsp(): 
    # todo 
    return "0.01%"

def duca_rrsp(): 
    # todo 
    return "0.01%"


def merged_rrsp_rates():
    merged_rates = [td_rrsp(), bmo_rrsp(), scotia_rrsp(), hsbc_rrsp(), nbc_rrsp(), simplii_rrsp(), eq_rrsp(),
                    motus_rrsp(), duca_rrsp(), meridian_rrsp(), motive_rrsp(), manulife_rrsp()]
    result = list(map(lambda x: round(float(x.strip("%")), 2), merged_rates))
    return merged_rates


def merged_rrsp_names():
    return ["TD", "BMO", "ScotiaBank", "HSBC", "NBC", "Simplii", "EQ", "Motus", "DUCA", "Meridian", "Motive",
            "Manulife"]

def rrsp_df(): 
    accounts = merged_rrsp_names()
    rates = merged_rrsp_rates()
    res = dict(zip(accounts,rates))
    
    df = pd.DataFrame(data=res, index=[0])
    
    return df

def main():
    #print(merged_rrsp_names(), merged_rrsp_rates())
    manulife_rrsp()

if __name__ == "__main__":
    main()
