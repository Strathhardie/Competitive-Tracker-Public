import json
import re

import requests
from bs4 import BeautifulSoup

# ToDo: Unit test cases for raw scraping, using table text or webpage text

'''
Retail Account Ranges (index value of the list element corrosponds to the below allocated ranges)
0    0 - 199
1    200 - 499
2    500 - 1k
3    1k - 3k
4    3k - 5k
5    5k - 10k
6    10k - 25k
7    25k - 50k
8    50k - 60k
9    60k - 100k
10   100k - 150k
11   150k+
'''

'''
Account Code Mapping

'CUPA':     CIBC - USD Personal Account
'CHISAUS':  CIBC - Renaissance High Interest Savings Account (USD)

'TDUSD':    TDCT - US$ Daily Interest Chequing
'TDUSB':    TDCT - US$ Borderless Account
'TDUSIS':   TDCT - Investment Savings Account (US$)

'RUSHIS':   RBC - US$ High Interest eSavings Account
'RUSPA':	RBC - US$ Personal Account
'RUSISA':   RBC - US$ Investment Savings Account

'BPRSA_US': BMO - US$ Premium Rate Savings Account

'BNSUSISA': BNS - US$ Investment Savings Account (Personal)
'BNSUSDIA': BNS - US$ Daily Interest Account

'TUSSAV':   Tangerine - US$ Savings Account

'ICUSHIS':  ICICI - US$ HiSave Savings Account

'MUSAA':	Manulife - US$ Advantage Account
'MUSISA':	Manulife - US$ Investment Savings Account

'HUSHRS':   HSBC - USD High Rate Savings 

'AUSCPA':   Altamira - US$ Cash Performer

'SCOUSA':   Scotia iTrade - Cash Optimizer US$ Account

'DUSD':     DUCA - US Dollar Account
'''

max_index = 12

def cibc_usd():
    url = 'https://www.cibconline.cibc.com/ebm-pno/api/v2/json/productRatesLegacy?lobId=3&sourceProductCode=CUPA'
    response = requests.request("GET", url)
    products = iter(['CUPA'])
    data = '{'
    for match in re.finditer(r"(rates : ([^}]+))", response.text):
        data = data + '"' + next(products) + '":' + match.group(2).replace("\'", "\"").replace('\n', '') + ","
    data = data[:-1]
    data += '}'
    raw_rates = json.loads(data)

    rates = {'CUPA': [0] * max_index}
    # CUPA
    for rate in raw_rates['CUPA']:
        if rate[1] == '0.0_up to_2999.99_CAD_Balance' and rate[6] == 1:
            for i in range(3):
                rates["CUPA"][i] = float(rate[3])
        elif rate[1] == '3000.0_-_9999.99_CAD_Balance' and rate[6] == 1:
            for i in range(3, 5):
                rates["CUPA"][i] = float(rate[3])
        elif rate[1] == '10000.0_-_24999.99_CAD_Balance' and rate[6] == 1:
            rates["CUPA"][5] = float(rate[3])
        elif rate[1] == '25000.0_-_59999.99_CAD_Balance' and rate[6] == 1:
            for i in range(6, 8):
                rates["CUPA"][i] = float(rate[3])
        elif rate[1] == '60000.0_and over_0.0_CAD_Portion' and rate[6] == 1:
            for i in range(8, max_index):
                rates["CUPA"][i] = float(rate[3])

    return rates


def cibc_broker_usd():
    url = 'https://www.renaissanceinvestments.ca/products/hisa'
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll("div", {"class": "hisa_rate"})[1].text
    rates = {}
    rates["CHISAUS"] = [float(re.findall('\d*\.?\d+', raw_data)[0])] * max_index
    return rates


def td_usd():
    url = "https://www.td.com/ca/en/personal-banking/products/bank-accounts/account-rates/"
    response = requests.request("GET", url)

    soup = BeautifulSoup(response.text, features="html.parser")
    tables = soup.findAll("table")

    rates = {'TDUSD': [0] * max_index, 'TDUSB': [0] * max_index}

    #TD USD Daily Interest Chequing Account
    raw_rates = []
    for tr in tables[8].find_all('tr')[1:]:
        td = tr.find_all('td')
        row = [i.text for i in td[1:]]
        raw_rates.append(re.findall('\d*\.?\d+', str(row))[0])

    raw_rates = [float(i) for i in raw_rates]
    for i in range(6):
        rates["TDUSD"][i] = raw_rates[i]

    rates["TDUSD"][6] = raw_rates[6]
    rates["TDUSD"][7] = raw_rates[6]

    for i in range(8, max_index):
        rates["TDUSD"][i] = raw_rates[7]

    #TD USD Borderless Plan
    raw_rates.clear()
    for tr in tables[9].find_all('tr')[1:]:
        td = tr.find_all('td')
        row = [i.text for i in td[1:]]
        raw_rates.append(re.findall('\d*\.?\d+', str(row))[0])

    raw_rates = [float(i) for i in raw_rates]
    for i in range(6):
        rates["TDUSB"][i] = raw_rates[i]

    rates["TDUSB"][6] = raw_rates[6]
    rates["TDUSB"][7] = raw_rates[6]

    for i in range(8, max_index):
        rates["TDUSB"][i] = raw_rates[7]


    return rates


def td_broker_usd():
    url = "https://www.td.com/ca/en/asset-management/additional-solutions/"
    response = requests.request("GET", url)

    soup = BeautifulSoup(response.text, features="html.parser")
    raw_rate = soup.findAll("table")[0].find_all('tr')[2].text

    # Regex pulls out any float value before a % sign
    rates = {'TDUSIS': [float(re.findall('\d*\.?\d+%', raw_rate)[0][:-1])] * max_index}
    return rates


def rbc_usd():
    url = "https://apps.royalbank.com/apps/app-services/public-rates/api/publicrates"
    response = requests.request("GET", url)
    raw_rates = json.loads(response.text)['result_content']

    rates = {}

    # RUSHIS
    for rate in raw_rates:
        if rate['Name'] == '0206850001':
            rates["RUSHIS"] = [float(rate['Value'])] * max_index
    # RUSPA
    for rate in raw_rates:
        if rate['Name'] == '0007170002':
            rates["RUSPA"] = [float(rate['Value'])] * max_index

    # RUSISA
    # Series A USD
    for rate in raw_rates:
        if rate['Name'] == '0273740002':
            rates["RUSISA"] = [float(rate['Value'])] * max_index

    return rates


def bmo_usd():
    url = "https://www.bmo.com/bmocda/templates/json_bankacct_include.jsp"
    response = requests.request("GET", url)
    # parses js vars into a list of valid json objects
    regex = r"var (([\S]+)([^;]+))"
    raw_data = re.findall(regex, response.text.replace('\'', '"').replace('\\x', 'x'))
    raw_rates = {match[1]: json.loads(match[2].lstrip('= ')) for match in raw_data}

    rates = {'BPRSA_US': [0] * max_index}

    for i in range(8):
        rates["BPRSA_US"][i] = float(raw_rates["PRSA_US"]["59999.99"]["value"])
    for i in range(8, max_index):
        rates["BPRSA_US"][i] = float(raw_rates["PRSA_US"]["99999999.99"]["value"])

    return rates


def bns_usd():
    url = "https://dmtsms.scotiabank.com/api/rates/daily/nonspecialaccountnew"
    response = requests.request("GET", url)
    raw_data = json.loads(response.text)
    rates = {"BNSUSDIA": [0] * max_index}

    for data in raw_data["data"]:
        if data["PRODUCT"] == "U.S. DOLLAR DAILY INTEREST":
            for i in range(3):
                rates["BNSUSDIA"][i] = data["TERMS"][0]['RATE']
            for i in range(3, 5):
                rates["BNSUSDIA"][i] = data["TERMS"][1]['RATE']
            rates["BNSUSDIA"][5] = data["TERMS"][2]['RATE']
            for i in range(6, max_index):
                rates["BNSUSDIA"][i] = data["TERMS"][3]['RATE']

    return rates


def bns_broker_usd():
    url = "https://ads.scotiabank.com/rate-history"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    tables = soup.findAll("table")
    raw_rate = tables[1].find_all("td", class_="pct")[0].text
    return {"BNSUSISA": [float(re.findall('\d*\.?\d+[ ]?%', raw_rate)[0][:-1])] * max_index}


def tangerine_usd():
    # Mappings: https://www.tangerine.ca/static_files/Tangerine_FBE/WebAssets/js/historical-rates.js
    import xml.etree.ElementTree as ET
    import datetime
    url = "https://www.tangerine.ca/historicalrates/RatesHistory.xml"
    response = requests.request("GET", url)
    rate = sorted(ET.fromstring(response.text).findall('.//product[@type="3010"][@currency="USD"]/rate'),
                  key=lambda x: datetime.datetime.strptime(x[0].text, '%m/%d/%Y'), reverse=True)[0]
    return {'TUSSAV': [float(re.findall('\d*\.?\d+', rate[1].attrib['en'][:-1])[0])] * max_index}


def icici_usd():
    url = "https://www.icicibank.ca/personal/hisave.page"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll("div", {"class": "rows clearfix"})[0].find_all("li")[1].text
    return {"ICUSHIS": [float(re.findall('\d*\.?\d+%', raw_data)[0][:-1])] * max_index}


def manulife_usd():
    url = "https://www.manulifebank.ca/bin/mbank/manulifeglobalrates.json"
    response = requests.request("GET", url)
    raw_data = json.loads(response.text)
    return {"MUSAA": [float(raw_data['rateUSADVA_0'])] * max_index,
            "MUSISA": [float(raw_data['rateUSISA_0'])] * max_index}


def hsbc_usd():
    url = "https://www.hsbc.ca/savings-accounts/rates/"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    rates = {"HUSHRS": [0] * max_index}

    raw_data = ''.join([tr.find_all("td")[0].text for tr in soup.findAll("table")[4].find_all("tr")[1:]])
    raw_rates = re.findall('\d*\.?\d+', raw_data)
    raw_rates = [float(i) for i in raw_rates]

    for i in range(6):
        rates["HUSHRS"][i] = raw_rates[0]
    rates["HUSHRS"][6] = raw_rates[1]
    for i in range(7, 9):
        rates["HUSHRS"][i] = raw_rates[2]
    for i in range(9, max_index):
        rates["HUSHRS"][i] = raw_rates[3]
    return rates


def altamira_usd():
    RefCode = "NBC101"
    url = "https://www.nbinvestments.ca/products/cashperformer.html"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_rate = 0
    for ele in soup.find_all("tr"):
        text = ele.text
        if RefCode in text:
            raw_rate = float(re.findall('\d*\.?\d+%', text)[0][:-1])
            break
    return {"AUSCPA": [raw_rate] * max_index}


def scotia_broker():
    url = "https://www.scotiaitrade.com/en/direct-investing-and-online-trading/trading-fees/commissions-and-fees.html"
    response = requests.request("GET", url)

    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll("table")[3].find_all('td')[2].text
    return {"SCOUSA": [float(re.findall('\d*\.?\d+%', raw_data)[0][:-1])] * max_index}


def duca_usd():
    url = "https://www.duca.com/rates"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll('table')[1].find_all('tr')
    rates = {"DUSD": [0] * max_index}

    raw_rates = raw_data[3].find_all('td')[1].text

    rates["DUSD"][1] = rates["DUSD"][2] = float(re.findall('\d*\.?\d+', raw_rates)[0])
    raw_rates = raw_data[4].find_all('td')[1].text
    for i in range(3, max_index):
        rates["DUSD"][i] = float(re.findall('\d*\.?\d+', raw_rates)[0])

    return rates


def mappings():
    account_info = [
        {
            'acc_code': "CUPA",
            'institution': "CIBC",
            'account_name': "USD Personal Account",
            'url': "https://www.cibc.com/en/interest-rates/personal-bank-account-rates.html?hpint_id=HP_IntRates-BankAccounts-E"},
        {
            'acc_code': "CHISAUS",
            'institution': "CIBC",
            'account_name': "Renaissance High Interest Savings Account (USD)",
            'url': "https://www.renaissanceinvestments.ca/products/hisa"},
        {
            'acc_code': "TDUSD",
            'institution': "TDCT",
            'account_name': "US$ Daily Interest Chequing",
            'url': "https://www.td.com/ca/en/personal-banking/products/bank-accounts/account-rates/"},
        {
            'acc_code': "TDUSB",
            'institution': "TDCT",
            'account_name': "US$ Borderless Account",
            'url': "https://www.td.com/ca/en/personal-banking/products/bank-accounts/account-rates/"},
        {
            'acc_code': "TDUSIS",
            'institution': "TDCT",
            'account_name': "Investment Savings Account (US$)",
            'url': "https://www.td.com/ca/en/asset-management/additional-solutions/"},
        {
            'acc_code': "RUSHIS",
            'institution': "RBC",
            'account_name': "US$ High Interest eSavings Account",
            'url': "https://www.rbcroyalbank.com/rates/persacct.html"},
        {
            'acc_code': "RUSPA",
            'institution': "RBC",
            'account_name': "US$ Personal Account",
            'url': "https://www.rbcroyalbank.com/rates/persacct.html"},
        {
            'acc_code': "RUSISA",
            'institution': "RBC",
            'account_name': "US$ Investment Savings Account",
            'url': "https://www.rbcroyalbank.com/products/isa/index.html"},
        {
            'acc_code': "BPRSA_US",
            'institution': "BMO",
            'account_name': "US$ Premium Rate Savings Account",
            'url': "https://www.bmo.com/bmocda/templates/json_bankacct_include.jsp"},
        {
            'acc_code': "BNSUSISA",
            'institution': "BNS",
            'account_name': "US$ Investment Savings Account (Personal)",
            'url': "https://ads.scotiabank.com/Rates"},
        {
            'acc_code': "BNSUSDIA",
            'institution': "BNS",
            'account_name': "US$ Daily Interest Account",
            'url': "https://www.scotiabank.com/ca/en/personal/rates-prices/savings-account-rates.html"},
        {
            'acc_code': "TUSSAV",
            'institution': "Tangerine",
            'account_name': "US$ Savings Account",
            'url': "https://www.tangerine.ca/en/rates/"},
        {
            'acc_code': "ICUSHIS",
            'institution': "ICICI",
            'account_name': "US$ HiSave Savings Account",
            'url': "https://www.icicibank.ca/personal/hisave.page"},
        {
            'acc_code': "MUSAA",
            'institution': "Manulife",
            'account_name': "US$ Advantage Account",
            'url': "https://www.manulifebank.ca/current-rates.html"},
        {
            'acc_code': "MUSISA",
            'institution': "Manulife",
            'account_name': "US$ Investment Savings Account",
            'url': "https://www.manulifebank.ca/personal-banking/investments/investment-savings.html"},
        {
            'acc_code': "HUSHRS",
            'institution': "HSBC",
            'account_name': "USD High Rate Savings",
            'url': "https://www.hsbc.ca/savings-accounts/rates/"},
        {
            'acc_code': "AUSCPA",
            'institution': "National Bank",
            'account_name': "Altamira U.S. CashPerformer Account",
            'url': "https://www.nbinvestments.ca/products/cashperformer.html"},
        {
            'acc_code': "SCOUSA",
            'institution': "Scotia iTrade",
            'account_name': "Cash Optimizer US$ Account",
            'url': "https://www.scotiaitrade.com/en/direct-investing-and-online-trading/trading-fees/commissions-and-fees.html"},
        {
            'acc_code': "DUSD",
            'institution': "DUCA",
            'account_name': "US Dollar Account",
            'url': "https://www.duca.com/rates"}

    ]
    return account_info


def index_range():
    return {"Range": ['0 - 199', '200 - 499', '500 - 1k', '1k - 3k', '3k - 5k', '5k - 10k', '10k - 25k', '25k - 50k',
                      '50k - 60k', '60k - 100k', '100k - 150k', '150k+']}


# ToDo: Exception handling, If module fails then recall.
def merged_usd_rates():
    merged_rates = {
        **index_range(),
        **cibc_usd(),
        **cibc_broker_usd(),
        **td_usd(),
        **td_broker_usd(),
        **rbc_usd(),
        **bmo_usd(),
        **bns_usd(),
        **bns_broker_usd(),
        **tangerine_usd(),
        **icici_usd(),
        **icici_usd(),
        **manulife_usd(),
        **hsbc_usd(),
        **altamira_usd(),
        **scotia_broker(),
        **duca_usd()
    }

    return merged_rates


def main():
    print(merged_usd_rates())

if __name__ == "__main__":
    main()
