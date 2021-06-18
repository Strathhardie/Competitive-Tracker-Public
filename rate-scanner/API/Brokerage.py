import json
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

# ToDo: Unit test cases for raw scraping, using table text or webpage text

'''
Retail Account Ranges (index value of the list element corrosponds to the below allocated ranges)
0    0 - 500
1    500 - 1k
2    1k - 3k
3    3k - 5k
4    5k - 10k
5    10k - 25k
6    25k - 50k
7    50k - 60k
8    60k - 100k
9    100k - 150k
10   150k+
'''

'''
Account Code Mapping

'CCTC':     CIBC - High Interest Savings Account (CTC)
'CHISA':    CIBC - Renaissance High Interest Savings Account

'TDISA':    TD - Investment Savings Account
'TDMC':     TD - Investment Savings Account (TDMC)
'TDPMC':    TD - Investment Savings Account (TDPMC) 
'TDCTC':    TD - Investment Savings Account (CTC)

'BNSISA':   BNS - Investment Savings Account (Personal)
'SCCOI':    Scotia iTrade - Cash Optimizer Investment

'RBCISA':   RBC - Investment Savings Account

'NBCISA':   NBC - Altamaria High-Interest Cash Performer

'MISA':     Manulife - Investment Savings Account

'B2BIIA':   B2B - High Interest Investment Account

'HTHISA':   HomeTrust - High Interest Savings Account Rate

'''


def cibc_wg():
    url = 'https://www.woodgundy.cibc.com/en/investing/high-interest-savings-account.html'
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll("span", {"class": "subheading-large"})[0].text
    rates = {}
    rates["CCTC"] = [float(re.findall('\d*\.?\d+', raw_data)[0])] * 11
    return rates


def cibc_hisa():
    url = 'https://www.renaissanceinvestments.ca/products/hisa'
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll("div", {"class": "hisa_rate"})[0].text
    rates = {}
    rates["CHISA"] = [float(re.findall('\d*\.?\d+', raw_data)[0])] * 11
    return rates


def td_broker():
    url = "https://www.td.com/ca/en/asset-management/additional-solutions/"
    response = requests.request("GET", url)

    rates = {"TDISA": None, "TDMC": None, "TDPMC": None, "TDCTC": None}

    soup = BeautifulSoup(response.text, features="html.parser")
    rows = soup.findAll("div", {"class": "td-chart-m"})[0].findAll("div", {"class": "td-chart-item-content"})[
        3].findAll("div", {"class": "rte"})
    for row in rows:
        if "TDB8150" in row.find('h4').text:
            rates["TDISA"] = [float(re.findall('\d*\.?\d+[ ]?%', row.text)[0][:-1])] * 11
        elif "TDB8155" in row.find('h4').text:
            rates["TDMC"] = [float(re.findall('\d*\.?\d+[ ]?%', row.text)[0][:-1])] * 11
        elif "TDB8157" in row.find('h4').text:
            rates["TDPMC"] = [float(re.findall('\d*\.?\d+[ ]?%', row.text)[0][:-1])] * 11
        elif "TDB8159" in row.find('h4').text:
            rates["TDCTC"] = [float(re.findall('\d*\.?\d+[ ]?%', row.text)[0][:-1])] * 11
    return rates


def bns_broker():
    url = "https://ads.scotiabank.com/rate-history"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    tables = soup.findAll("table")
    raw_rate = tables[0].find_all("td", class_="pct")[0].text
    return {"BNSISA": [float(re.findall('\d*\.?\d+[ ]?%', raw_rate)[0][:-1])] * 11}


def rbc_broker():
    # https://www.rbcroyalbank.com/products/isa/index.html
    url = "https://apps.royalbank.com/apps/app-services/public-rates/api/publicrates"
    response = requests.request("GET", url)
    raw_rates = json.loads(response.text)['result_content']

    # RBCISA
    for rate in raw_rates:
        if rate['Name'] == '0245410003':
            return {"RBCISA": [float(rate['Value'])] * 11}


def manulife_broker():
    # https://www.manulifebank.ca/personal-banking/investments/investment-savings.html
    url = "https://www.manulifebank.ca/bin/mbank/manulifeglobalrates.json"
    response = requests.request("GET", url)
    raw_data = json.loads(response.text)
    return {"MISA": [float(raw_data['rateISA_0'])] * 11}


def altamira_broker():
    url = 'https://www.nbinvestments.ca/products/cashperformer.html'
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    rows = soup.findAll("tr")
    for row in rows:
        # FundSERV code
        if "NBC100" in row.text:
            return {"NBCISA": [float(re.findall('\d*\.?\d+[ ]?%', row.text)[0][:-1])] * 11}


def b2b_broker():
    url = 'https://b2bbank.com/advisor-broker-rates/banking-rates'
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    rows = soup.findAll("tr")
    for row in rows:
        if "HIIA" in row.text:
            raw_rate = row.find_all('td')[1].text
            return {"B2BIIA": [float(re.findall('\d*\.?\d+[ ]?%', raw_rate)[0][:-1])] * 11}


def hometrust_broker():
    url = 'https://www.hometrust.ca/deposits/hisa/'
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.find_all("header")[1].text
    return {"HTHISA": [float(re.findall('\d*\.?\d+[ ]?%', raw_data)[0][:-1])] * 11}


def scotia_broker():
    url = "https://www.scotiaitrade.com/en/direct-investing-and-online-trading/trading-fees/commissions-and-fees.html"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    rows = soup.findAll("tr")

    for row in rows:
        if "Cash Optimizer Investment Account" in row.text:
            raw_rate = row.find_all('td')[1].text
            return {"SCCOI": [float(re.findall('\d*\.?\d+[ ]?%', raw_rate)[0][:-1])] * 11}


def mappings():
    account_info = [
        {
            'acc_code': 'CCTC',
            'account_name': 'High Interest Savings Account (CTC)',
            'institution': 'CIBC',
            'url': 'https://www.woodgundy.cibc.com/en/investing/high-interest-savings-account.html'},
        {
            'acc_code': 'CHISA',
            'account_name': 'Renaissance High Interest Savings Account',
            'institution': 'CIBC',
            'url': 'https://www.renaissanceinvestments.ca/products/hisa'},
        {
            'acc_code': 'TDISA',
            'account_name': 'Investment Savings Account',
            'institution': 'TD',
            'url': 'https://www.td.com/ca/en/asset-management/additional-solutions/'},
        {
            'acc_code': 'TDMC',
            'account_name': 'Investment Savings Account (TDMC)',
            'institution': 'TD',
            'url': 'https://www.td.com/ca/en/asset-management/additional-solutions/'},
        {
            'acc_code': 'TDPMC',
            'account_name': 'Investment Savings Account (TDPMC)',
            'institution': 'TD',
            'url': 'https://www.td.com/ca/en/asset-management/additional-solutions/'},
        {
            'acc_code': 'TDCTC',
            'account_name': 'Investment Savings Account (CTC)',
            'institution': 'TD',
            'url': 'https://www.td.com/ca/en/asset-management/additional-solutions/'},
        {
            'acc_code': 'BNSISA',
            'account_name': 'Investment Savings Account (Personal)',
            'institution': 'BNS',
            'url': 'https://ads.scotiabank.com/rates'},
        {
            'acc_code': 'SCCOI',
            'account_name': 'Cash Optimizer Investment',
            'institution': 'Scotia iTrade',
            'url': 'https://www.scotiaitrade.com/en/direct-investing-and-online-trading/trading-fees/commissions-and-fees.html'},
        {
            'acc_code': 'RBCISA',
            'account_name': 'Investment Savings Account',
            'institution': 'RBC',
            'url': 'https://www.rbcroyalbank.com/products/isa/index.html'},
        {
            'acc_code': 'NBCISA',
            'account_name': 'Altamaria High-Interest Cash Performer',
            'institution': 'NBC',
            'url': 'https://www.nbinvestments.ca/products/cashperformer.html'},
        {
            'acc_code': 'MISA',
            'account_name': 'Investment Savings Account',
            'institution': 'Manulife',
            'url': 'https://www.manulifebank.ca/personal-banking/investments/investment-savings.html'},
        {
            'acc_code': 'B2BIIA',
            'account_name': 'High Interest Investment Account',
            'institution': 'B2B',
            'url': 'https://b2bbank.com/advisor-broker-rates/banking-rates'},
        {
            'acc_code': 'HTHISA',
            'account_name': 'High Interest Savings Account Rate',
            'institution': 'HomeTrust',
            'url': 'https://www.hometrust.ca/deposits/hisa/'}]

    return account_info


def index_range():
    return {"Range": ['0 - 500', '500 - 1k', '1k - 3k', '3k - 5k', '5k - 10k', '10k - 25k', '25k - 50k', '50k - 60k',
                      '60k - 100k', '100k - 150k', '150k+']}


def merged_brokerage_rates():
    merged_rates = {
        **index_range(),
        **cibc_wg(),
        **cibc_hisa(),
        **td_broker(),
        **bns_broker(),
        **rbc_broker(),
        **manulife_broker(),
        **altamira_broker(),
        **b2b_broker(),
        **hometrust_broker(),
        **scotia_broker()
    }
    return merged_rates

def brokerage_df(): 
    df = pd.DataFrame(data=merged_brokerage_rates())
    return df

def main():
    print(brokerage_df())


if __name__ == "__main__":
    main()
