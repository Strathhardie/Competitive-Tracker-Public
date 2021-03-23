import json
import re

import requests
from bs4 import BeautifulSoup

# ToDo: Unit test cases for raw scraping, using table text or webpage text

'''
Retail Account Ranges (index value of the list element corrosponds to the below allocated ranges)
0    0 - 1k
1    1k - 3k
2    3k - 5k
3    5k - 10k
4    10k - 25k
5    25k - 50k
6    50k - 60k
7    60k - 100k
8    100k - 150k
9    150k - 250k
10   250k - 500k
11   500k - 1M
12   1M - 5M
13   5M+
'''

'''
Account Code Mapping

'BSBA': BMO - Savings Builder Account 
'BSS': BMO -  Smart Saver
'BPRSA': BMO - Premium Rate Savings Account

'CESA': CIBC - eAdvantage Savings Account
'CBSA': CIBC - Bonus Savings Account
'CBPGA': CIBC - Premium Growth Account
'CAY': CIBC - CIBC Advantage® for Youth

'ESA': TD - Everyday Savings Account
'HISA': TD - High Interest Savings Account
'PSA': TD - ePremium Savings Account
'YCA': TD - Youth Checquing Account

'RHIS': RBC - High Interest eSavings
'RES': RBC - Enhanced Savings
'RDDS': RBC - Day to Day Savings Account
'RLYSA': RBC - Leo Young Savings Account

'BNSMPS': BNS - Momentum Plus Savings
'BNSMM': BNS - Money Master
'BNSSANR': BNS - Savings Accelerator - Non Reg
'BNSSATF': BNS - Savings Accelerator -  Tax Free

'TSAV': Tangerine - Savings Acount

'ICHIS': ICICI - HiSave Savings
'ICPS': ICICI - Premium Savings
'ICYSS': ICICI - Young Stars Savings

'MAA': Manulife  - Advantage Account

'NSPSA': NBC - Special Project Savings Account*
'NYS': NBC - Youth savings*
'NDSA': NBC - Daily interest savings account*
'NHISA': NBC - High Interest Savings Account

'SHISA': Simplii - High Interest Savings Account

'HCDSA': HSBC - Canadian Dollar Savings Accounts

'CTHISA': CDN TIRE - High Interest Savings

'MCHISA': Meridian Credit - Union High Interest Savings Account 

'EQSPA': EQ Bank - Savings Plus Account

'WSHISC': Wealthsimple - High Interest Savings Cash

'LBCHISA': Laurentian Bank - High Interest Savings Tiered

'MBHISA': Motusbank - High Interest Savings Account

'MFMSA': Motive Financial - Motive Savvy Savings Account

'DRSA': DUCA - Regular Savings Account
'DUSD': DUCA - US Dollar Account
'DEMSA': DUCA - Earn More Savings Account 


'''

max_index = 14

def cibc_retail():
    url = 'https://www.cibconline.cibc.com/ebm-pno/api/v2/json/productRatesLegacy?lobId=3&sourceProductCode=CESA,CBSA,CBPGA'
    response = requests.request("GET", url)

    products = iter(['CBSA', 'CBPGA', 'CESA'])

    data = '{'
    for match in re.finditer(r"(rates : ([^}]+))", response.text):
        data = data + '"' + next(products) + '":' + match.group(2).replace("\'", "\"").replace('\n', '') + ","
    data = data[:-1]
    data += '}'
    raw_rates = json.loads(data)

    rates = {"CESA": [0] * max_index, "CBSA": [0] * max_index, "CBPGA": [0] * max_index, "CAY": [0] * max_index}
    # CESA
    for rate in raw_rates['CESA']:
        if '0.0_up to_4999.99_CAD_Balance' in rate:
            for i in range(3):
                rates["CESA"][i] = float(rate[3])
        elif '5000.0_and over_0.0_CAD_Balance' in rate:
            for i in range(3, max_index):
                rates["CESA"][i] = float(rate[3])

    # CBSA
    for rate in raw_rates['CBSA']:
        if '0.0_up to_2999.99_CAD_Balance' in rate:
            for i in range(2):
                rates["CBSA"][i] = float(rate[3])
        elif '3000.0_and over_0.0_CAD_Balance' in rate:
            for i in range(2, max_index):
                rates["CBSA"][i] = float(rate[3])

    # CBPGA
    for rate in raw_rates['CBPGA']:
        if rate[2] == 1 and rate[6] == 1:
            for i in range(max_index):
                rates["CBPGA"][i] = float(rate[3])
        elif rate[2] == 1 and rate[6] == 3:
            for i in range(max_index):
                rates["CAY"][i] = float(rate[3])

    return rates


def td_retail():
    url = "https://www.td.com/ca/en/personal-banking/products/bank-accounts/account-rates/"
    response = requests.request("GET", url)

    soup = BeautifulSoup(response.text, features="html.parser")
    tables = soup.findAll("table")

    rates = {'ESA': [0] * max_index, 'HISA': [0] * max_index, 'PSA': [0] * max_index, 'YCA': [0] * max_index}
    # ESA
    raw_rates = []
    for tr in tables[0].find_all('tr')[1:]:
        td = tr.find_all('td')
        row = [i.text for i in td[1:]]
        raw_rates.append(re.findall('\d*\.?\d+', str(row))[0])
    raw_rates = [float(i) for i in raw_rates]

    rates["ESA"][0] = raw_rates[0]
    rates["ESA"][1] = raw_rates[1]
    rates["ESA"][2] = raw_rates[1]
    rates["ESA"][3] = raw_rates[2]
    rates["ESA"][4] = raw_rates[3]
    rates["ESA"][5] = raw_rates[4]
    rates["ESA"][6] = raw_rates[4]
    for i in range(7, max_index):
        rates["ESA"][i] = raw_rates[5]

    # HISA
    raw_rates = []
    for tr in tables[1].find_all('tr')[1:]:
        td = tr.find_all('td')
        row = [i.text for i in td[1:]]
        raw_rates.append(re.findall('\d*\.?\d+', str(row))[0])
    raw_rates = [float(i) for i in raw_rates]

    for i in range(3):
        rates["HISA"][i] = raw_rates[0]
    for i in range(3, 6):
        rates["HISA"][i] = raw_rates[1]
    for i in range(6, 8):
        rates["HISA"][i] = raw_rates[2]
    for i in range(8, 10):
        rates["HISA"][i] = raw_rates[3]
    for i in range(10, 12):
        rates["HISA"][i] = raw_rates[4]
    for i in range(12, max_index):
        rates["HISA"][i] = raw_rates[5]

    # PSA
    raw_rates = []
    for tr in tables[2].find_all('tr')[1:]:
        td = tr.find_all('td')
        row = [i.text for i in td[1:]]
        raw_rates.append(re.findall('\d*\.?\d+', str(row))[0])
    raw_rates = [float(i) for i in raw_rates]

    for i in range(4):
        rates["PSA"][i] = raw_rates[0]
    for i in range(4, 6):
        rates["PSA"][i] = raw_rates[1]
    for i in range(6, 8):
        rates["PSA"][i] = raw_rates[2]
    for i in range(8, 10):
        rates["PSA"][i] = raw_rates[3]
    for i in range(10, 12):
        rates["PSA"][i] = raw_rates[4]
    for i in range(12, max_index):
        rates["PSA"][i] = raw_rates[5]

    # YCA
    raw_rates = []
    for tr in tables[6].find_all('tr')[1:]:
        td = tr.find_all('td')
        row = [i.text for i in td[1:]]
        raw_rates.append(re.findall('\d*\.?\d+', str(row))[0])
    raw_rates = [float(i) for i in raw_rates]

    for i in range(3):
        rates["YCA"][i] = raw_rates[0]
    for i in range(3, max_index):
        rates["YCA"][i] = raw_rates[1]

    return rates


def rbc_retail():
    url = "https://apps.royalbank.com/apps/app-services/public-rates/api/publicrates"
    response = requests.request("GET", url)
    raw_rates = json.loads(response.text)['result_content']

    rates = {'RHIS': [0] * 14, 'RES': [0] * 14, 'RDDS': [0] * 14, 'RLYSA': [0] * 14}

    # RHIS
    for rate in raw_rates:
        if rate['Name'] == '0026840006':
            for i in range(14):
                rates["RHIS"][i] = float(rate['Value'])

    # RES
    for rate in raw_rates:
        if rate['Name'] == '0006940002':
            for i in range(3):
                rates["RES"][i] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0006940003':
            rates["RES"][3] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0006940004':
            rates["RES"][4] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0006940005':
            for i in range(5, 7):
                rates["RES"][i] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0006940006':
            rates["RES"][7] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0006940007':
            rates["RES"][8] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0006940008':
            rates["RES"][9] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0006940009':
            for i in range(10, 14):
                rates["RES"][i] = float(rate['Value'])

    # RDDS
    for rate in raw_rates:
        if rate['Name'] == '0006870002':
            rates["RDDS"][0] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0006870003':
            rates["RDDS"][1] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0006870004':
            rates["RDDS"][2] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0006870005':
            for i in range(3, 14):
                rates["RDDS"][i] = float(rate['Value'])

    # RLYSA
    for rate in raw_rates:
        if rate['Name'] == '0217360001':
            rates["RLYSA"][0] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0217360002':
            rates["RLYSA"][1] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0217360003':
            rates["RLYSA"][2] = float(rate['Value'])
    for rate in raw_rates:
        if rate['Name'] == '0217360004':
            for i in range(3, 14):
                rates["RLYSA"][i] = float(rate['Value'])

    return rates


# List outputs need to be displayed as it is for bonus rate
def bmo_retail():
    # https://www.bmo.com/main/personal/bank-accounts/savings/interest-rates/
    url = "https://www.bmo.com/bmocda/templates/json_bankacct_include.jsp"
    response = requests.request("GET", url)
    # parses js vars into a list of valid json objects
    regex = r"var (([\S]+)([^;]+))"
    raw_data = re.findall(regex, response.text.replace('\'', '"').replace('\\x', 'x'))
    raw_rates = {match[1]: json.loads(match[2].lstrip('= ')) for match in raw_data}

    rates = {'BSBA': [], 'BSS': [0] * 14, 'BPRSA': [0] * 14}

    for i in range(10):
        rates['BSBA'].append([float(raw_rates["SBA_CA"]["value"]), float(raw_rates["SBAB_CA"]["250000"]["value"])])
    for i in range(10, 14):
        rates['BSBA'].append(float(raw_rates["SBA_CA"]["value"]) + float(raw_rates["SBAB_CA"]["99999999.99"]["value"]))

    for i in range(3):
        rates["BSS"][i] = float(raw_rates["OPRS_CA"]["4999.99"]["value"])
    for i in range(3, 14):
        rates["BSS"][i] = float(raw_rates["OPRS_CA"]["99999999.99"]["value"])

    for i in range(7):
        rates["BPRSA"][i] = float(raw_rates["PRSA_CA"]["59999.99"]["value"])
    for i in range(7, 14):
        rates["BPRSA"][i] = float(raw_rates["PRSA_CA"]["99999999.99"]["value"])

    return rates


# Special Visualization Condition with Momentum Plus Account
def bns_retail():
    url = "https://dmtsms.scotiabank.com/api/rates/daily/nonspecialaccountnew"
    response = requests.request("GET", url)
    raw_data = json.loads(response.text)
    rates = {"BNSMPS": None, "BNSMM": [0] * 14, "BNSSANR": [0] * 14, "BNSSATF": [0] * 14}

    for data in raw_data["data"]:
        if data["PRODUCT"] == "MONEY MASTER SAVINGS":
            for i in range(3):
                rates["BNSMM"][i] = data["TERMS"][0]['RATE']
            for i in range(3, 14):
                rates["BNSMM"][i] = data["TERMS"][1]['RATE']
        # Savings Accelerator - Non Reg
        elif data["PRODUCT"] == "INVESTMENT PLATFORM HISA NON-REG PER.CAD":
            for i in range(10):
                rates["BNSSANR"][i] = data["TERMS"][0]['RATE']
            for i in range(10, 14):
                rates["BNSSANR"][i] = data["TERMS"][1]['RATE']
        # Savings Accelerator - Tax Free
        elif data["PRODUCT"] == "INVESTMENT PLATFORM HISA TFSA CAD":
            for i in range(10):
                rates["BNSSATF"][i] = data["TERMS"][0]['RATE']
            for i in range(10, 14):
                rates["BNSSATF"][i] = data["TERMS"][1]['RATE']

    url = "https://dmtsms.scotiabank.com/api/rates/daily/mompsaving"
    response = requests.request("GET", url)
    raw_data = json.loads(response.text)
    raw_rate = [0, 0, 0]
    for data in raw_data["data"]:
        if data["LABEL"] == "Regular":
            raw_rate[0] = data["RATE"]
        elif data["LABEL"] == "360D Premium":
            raw_rate[1] = data["RATE"]
        elif data["LABEL"] == "Booster Ultimate":
            raw_rate[2] = data["RATE"]
    rates["BNSMPS"] = [raw_rate] * 14
    return rates


def tangerine_retail():
    import xml.etree.ElementTree as ET
    import datetime
    url = "https://www.tangerine.ca/historicalrates/RatesHistory.xml"
    response = requests.request("GET", url)
    rate = sorted(ET.fromstring(response.text).findall('.//product[@type="3000"][@currency="CAD"]/rate'),
                  key=lambda x: datetime.datetime.strptime(x[0].text, '%m/%d/%Y'), reverse=True)[0]
    return {'TSAV': [float(re.findall('\d*\.?\d+', rate[1].attrib['en'][:-1])[0])] * 14}


def icici_retail():
    url = "http://www.icicibank.ca/personalbanking/popup_sav.page?#toptitle"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    products = iter(["ICHIS", "ICPS", "ICYSS"])
    rates = {}
    raw_rates = soup.findAll("table")[0].find_all('tr')[1:][0].find_all('td')[1:]
    for data in raw_rates:
        rates[next(products)] = [float(re.findall('\d*\.?\d+', data.text)[0])] * 14
    return rates


def manulife_retail():
    url = "https://www.manulifebank.ca/bin/mbank/manulifeglobalrates.json"
    response = requests.request("GET", url)
    raw_data = json.loads(response.text)
    return {"MAA": [float(raw_data['rateADVA_0'])] * 14}


def nbc_retail():
    url = "https://www.nbc.ca/en/rates-and-analysis/interest-rates-and-returns/bank-accounts.html"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    products = iter(["NSPSA", "NYS", "NDSA", "NHISA"])
    rates = {}

    # NSPSA, NYS, NDSA
    raw_rates = [float(tr.find_all('td')[1:][0].text) for tr in soup.findAll("table")[0].find_all('tr')[1:4]]
    for rate in raw_rates:
        rates[next(products)] = [rate] * 14

    # NHISA
    raw_rates = soup.findAll("table")[2].find_all('tr')[1:][0].find_all('td')[1:][0].text
    rates[next(products)] = [float(raw_rates)] * 14
    return rates


def simplii_retail():
    url = "https://online.simplii.com/ebm-pno/api/v2/json/rates/ALL"
    response = requests.request("GET", url)
    raw_data = json.loads(response.text)
    return {"SHISA": [raw_data[4]['interestRates'][1]['rateValue']] * 14}


def hsbc_retail():
    url = "https://www.hsbc.ca/savings-accounts/rates/"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    rates = {"HCDSA": [0] * 14}
    raw_data = ''.join([tr.find_all("td")[0].text for tr in soup.findAll("table")[0].find_all("tr")[1:]])
    raw_rates = re.findall('\d*\.?\d+', raw_data)
    raw_rates = [float(i) for i in raw_rates]

    for i in range(5):
        rates["HCDSA"][i] = raw_rates[0]
    rates["HCDSA"][5] = raw_rates[1]
    for i in range(6, 8):
        rates["HCDSA"][i] = raw_rates[2]
    for i in range(8, 14):
        rates["HCDSA"][i] = raw_rates[3]
    return rates


def cdntire_retail():
    url = "https://www.myctfs.com/Rates/SavingsRates/"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll("table")[0].find_all("tr")[1:][0].find_all("td")[0].text
    return {"CTHISA": [float(re.findall('\d*\.?\d+', raw_data)[0])] * 14}


def meridian_retail():
    url = "https://www.meridiancu.ca/Personal/Meridian-Rates-Fees.aspx"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll("table")[0].find_all("tr")[1:][0].find_all('td')[0].text
    return {"MCHISA": [float(re.findall('\d*\.?\d+', raw_data)[0])] * 14}


def eqbank_retail():
    url = "https://www.eqbank.ca/personal-banking/features-rates"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll("div", {"class": "copy"})[0].find_all("li")
    rates = {"EQSPA": [0] * 14}
    for data in raw_data:
        if "%" in data.text:
            rates["EQSPA"] = [float(re.findall('\d*\.?\d+', data.text)[0])] * 14
            break
    return rates


#Unreliable but only source(FAQ Article)
def wealthsimple_retail():
    url = "https://help.wealthsimple.com/hc/en-ca/articles/360058456853-Can-you-tell-me-more-about-the-interest-rate-on-the-Wealthsimple-Cash-account-"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll("div", {"class": "article-body"})[0].find_all("p")[0].text
    return {"WSHISC": [float(re.findall('\d*\.?\d+%', raw_data)[0][:-1])] * 14}


def laurentianbank_retail():
    url = "https://www.lbcdigital.ca/en/saving/high-interest-savings-account"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.find('table').find_all('td')
    rates = {"LBCHISA": [0] * 14}
    for i in range(6):
        rates["LBCHISA"][i] = float(re.findall('\d*\.?\d+', raw_data[1].text)[0])
    for i in range(6, 14):
        rates["LBCHISA"][i] = float(re.findall('\d*\.?\d+', raw_data[3].text)[0])
    return rates


def motusbank_retail():
    url = "https://www.motusbank.ca/Support/Rates"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.find("a", {"data-gtm-label": "406550360"}).find_parent('div').find('h5').text
    return {"MBHISA": [float(re.findall('\d*\.?\d+', raw_data)[0])] * 14}


def motivefinancial_retail():
    url = "https://www.motivefinancial.com/Rates/"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    rates = {"MFMSA": [0] * 14}
    raw_data = [td.text for td in soup.findAll("table")[1].find_all("td")[1:][::2]]
    for i in range(13):
        rates["MFMSA"][i] = float(re.findall('\d*\.?\d+', raw_data[0])[0])
    rates["MFMSA"][13] = float(re.findall('\d*\.?\d+', raw_data[1])[0])
    return rates


def duca_retail():
    url = "https://www.duca.com/rates"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll('table')[1].find_all('tr')
    rates = {"DRSA": [0] * 14, "DUSD": [0] * 14, "DEMSA": [0] * 14}

    # DRSA
    raw_rates = raw_data[1].find_all('td')[1].text
    rates["DRSA"] = [float(re.findall('\d*\.?\d+', raw_rates)[0])] * 14

    # DUSD
    raw_rates = raw_data[3].find_all('td')[1].text
    for i in range(3):
        rates["DUSD"][i] = float(re.findall('\d*\.?\d+', raw_rates)[0])
    raw_rates = raw_data[4].find_all('td')[1].text
    for i in range(3, 14):
        rates["DUSD"][i] = float(re.findall('\d*\.?\d+', raw_rates)[0])

    # DEMSA
    raw_data = soup.findAll('table')[2].find_all('tr')[1].find_all('td')[1].text
    rates["DEMSA"] = [float(re.findall('\d*\.?\d+', raw_rates)[0])] * 14

    return rates


def mappings():
    account_info = [{'acc_code': 'BSBA',
                     'account_name': 'Savings Builder Account',
                     'institution': 'BMO',
                     'url': 'https://www.bmo.com/main/personal/bank-accounts/savings/interest-rates/'},
                    {'acc_code': 'BSS',
                     'account_name': 'Smart Saver',
                     'institution': 'BMO',
                     'url': 'https://www.bmo.com/main/personal/bank-accounts/savings/interest-rates/'},
                    {'acc_code': 'BPRSA',
                     'account_name': 'Premium Rate Savings Account',
                     'institution': 'BMO',
                     'url': 'https://www.bmo.com/main/personal/bank-accounts/savings/interest-rates/'},
                    {'acc_code': 'CESA',
                     'account_name': 'eAdvantage Savings Account',
                     'institution': 'CIBC',
                     'url': 'https://www.cibc.com/en/interest-rates/personal-bank-account-rates.html'},
                    {'acc_code': 'CBSA',
                     'account_name': 'Bonus Savings Account',
                     'institution': 'CIBC',
                     'url': 'https://www.cibc.com/en/interest-rates/personal-bank-account-rates.html'},
                    {'acc_code': 'CBPGA',
                     'account_name': 'Premium Growth Account',
                     'institution': 'CIBC',
                     'url': 'https://www.cibc.com/en/interest-rates/personal-bank-account-rates.html'},
                    {'acc_code': 'CAY',
                     'account_name': 'Advantage® for Youth',
                     'institution': 'CIBC',
                     'url': 'https://www.cibc.com/en/interest-rates/personal-bank-account-rates.html'},
                    {'acc_code': 'ESA',
                     'account_name': 'Everyday Savings Account',
                     'institution': 'TD',
                     'url': 'https://www.td.com/ca/en/personal-banking/products/bank-accounts/account-rates/'},
                    {'acc_code': 'HISA',
                     'account_name': 'High Interest Savings Account',
                     'institution': 'TD',
                     'url': 'https://www.td.com/ca/en/personal-banking/products/bank-accounts/account-rates/'},
                    {'acc_code': 'PSA',
                     'account_name': 'ePremium Savings Account',
                     'institution': 'TD',
                     'url': 'https://www.td.com/ca/en/personal-banking/products/bank-accounts/account-rates/'},
                    {'acc_code': 'YCA',
                     'account_name': 'Youth Checquing Account',
                     'institution': 'TD',
                     'url': 'https://www.td.com/ca/en/personal-banking/products/bank-accounts/account-rates/'},
                    {'acc_code': 'RHIS',
                     'account_name': 'High Interest eSavings',
                     'institution': 'RBC',
                     'url': 'https://www.rbcroyalbank.com/rates/persacct.html'},
                    {'acc_code': 'RES',
                     'account_name': 'Enhanced Savings',
                     'institution': 'RBC',
                     'url': 'https://www.rbcroyalbank.com/rates/persacct.html'},
                    {'acc_code': 'RDDS',
                     'account_name': 'Day to Day Savings Account',
                     'institution': 'RBC',
                     'url': 'https://www.rbcroyalbank.com/rates/persacct.html'},
                    {'acc_code': 'RLYSA',
                     'account_name': 'Leo Young Savings Account',
                     'institution': 'RBC',
                     'url': 'https://www.rbcroyalbank.com/rates/persacct.html'},
                    {'acc_code': 'BNSMPS',
                     'account_name': 'Momentum Plus Savings',
                     'institution': 'BNS',
                     'url': 'https://www.scotiabank.com/ca/en/personal/rates-prices/savings-account-rates.html'},
                    {'acc_code': 'BNSMM',
                     'account_name': 'Money Master',
                     'institution': 'BNS',
                     'url': 'https://www.scotiabank.com/ca/en/personal/rates-prices/savings-account-rates.html'},
                    {'acc_code': 'BNSSANR',
                     'account_name': 'Savings Accelerator - Non Reg',
                     'institution': 'BNS',
                     'url': 'https://www.scotiabank.com/ca/en/personal/rates-prices/savings-account-rates.html'},
                    {'acc_code': 'BNSSATF',
                     'account_name': 'Savings Accelerator -  Tax Free',
                     'institution': 'BNS',
                     'url': 'https://www.scotiabank.com/ca/en/personal/rates-prices/savings-account-rates.html'},
                    {'acc_code': 'TSAV',
                     'account_name': 'Savings Acount',
                     'institution': 'Tangerine',
                     'url': 'https://www.tangerine.ca/en/rates/'},
                    {'acc_code': 'ICHIS',
                     'account_name': 'HiSave Savings',
                     'institution': 'ICICI',
                     'url': 'https://www.icicibank.ca/personalbanking/popup_sav.page'},
                    {'acc_code': 'ICPS',
                     'account_name': 'Premium Savings',
                     'institution': 'ICICI',
                     'url': 'https://www.icicibank.ca/personalbanking/popup_sav.page'},
                    {'acc_code': 'ICYSS',
                     'account_name': 'Young Stars Savings',
                     'institution': 'ICICI',
                     'url': 'https://www.icicibank.ca/personalbanking/popup_sav.page'},
                    {'acc_code': 'MAA',
                     'account_name': 'Advantage Account',
                     'institution': 'Manulife',
                     'url': 'https://www.manulifebank.ca/current-rates.html'},
                    {'acc_code': 'NSPSA',
                     'account_name': 'Special Project Savings Account*',
                     'institution': 'NBC',
                     'url': 'https://www.nbc.ca/en/rates-and-analysis/interest-rates-and-returns/bank-accounts.html'},
                    {'acc_code': 'NYS',
                     'account_name': 'Youth savings*',
                     'institution': 'NBC',
                     'url': 'https://www.nbc.ca/en/rates-and-analysis/interest-rates-and-returns/bank-accounts.html'},
                    {'acc_code': 'NDSA',
                     'account_name': 'Daily interest savings account*',
                     'institution': 'NBC',
                     'url': 'https://www.nbc.ca/en/rates-and-analysis/interest-rates-and-returns/bank-accounts.html'},
                    {'acc_code': 'NHISA',
                     'account_name': 'High Interest Savings Account',
                     'institution': 'NBC',
                     'url': 'https://www.nbc.ca/en/rates-and-analysis/interest-rates-and-returns/bank-accounts.html'},
                    {'acc_code': 'SHISA',
                     'account_name': 'High Interest Savings Account',
                     'institution': 'Simplii',
                     'url': 'https://www.simplii.com/en/rates/high-interest-savings-account-rates.html'},
                    {'acc_code': 'HCDSA',
                     'account_name': 'Canadian Dollar Savings Accounts',
                     'institution': 'HSBC',
                     'url': 'https://www.hsbc.ca/savings-accounts/rates/'},
                    {'acc_code': 'CTHISA',
                     'account_name': 'High Interest Savings',
                     'institution': 'CDN TIRE',
                     'url': 'https://www.myctfs.com/Rates/'},
                    {'acc_code': 'MCHISA',
                     'account_name': 'Union High Interest Savings Account',
                     'institution': 'Meridian Credit',
                     'url': 'https://www.meridiancu.ca/Personal/Meridian-Rates-Fees.aspx'},
                    {'acc_code': 'EQSPA',
                     'account_name': 'Savings Plus Account',
                     'institution': 'EQ Bank',
                     'url': 'https://www.eqbank.ca/personal-banking/features-rates'},
                    {'acc_code': 'WSHISC',
                     'account_name': 'High Interest Savings Cash',
                     'institution': 'Wealthsimple',
                     'url': 'https://help.wealthsimple.com/hc/en-ca/articles/360058456853-Can-you-tell-me-more-about-the-interest-rate-on-the-Wealthsimple-Cash-account-'},
                    {'acc_code': 'LBCHISA',
                     'account_name': 'High Interest Savings Tiered',
                     'institution': 'Laurentian Bank',
                     'url': 'https://www.lbcdigital.ca/en/saving/high-interest-savings-account'},
                    {'acc_code': 'MBHISA',
                     'account_name': 'High Interest Savings Account',
                     'institution': 'Motusbank',
                     'url': 'https://www.motusbank.ca/Support/Rates'},
                    {'acc_code': 'MFMSA',
                     'account_name': 'Motive Savvy Savings Account',
                     'institution': 'Motive Financial',
                     'url': 'https://www.motivefinancial.com/Rates/'},
                    {'acc_code': 'DRSA',
                     'account_name': 'Regular Savings Account',
                     'institution': 'DUCA',
                     'url': 'https://www.duca.com/rates'},
                    {'acc_code': 'DUSD',
                     'account_name': 'US Dollar Account',
                     'institution': 'DUCA',
                     'url': 'https://www.duca.com/rates'},
                    {'acc_code': 'DEMSA',
                     'account_name': 'Earn More Savings Account',
                     'institution': 'DUCA',
                     'url': 'https://www.duca.com/rates'}]

    return account_info


def index_range():
    return {"Range": ['0 - 1k', '1k - 3k', '3k - 5k', '5k - 10k', '10k - 25k', '25k - 50k', '50k - 60k', '60k - 100k',
                      '100k - 150k', '150k - 250k', '250k - 500k', '500k - 1M', '1M - 5M', '5M+']}


# ToDo: Exception handling, If module fails then recall.
def merged_retail_rates():
    merged_rates = {
        **index_range(),
        **cibc_retail(),
        **bmo_retail(),
        **td_retail(),
        **rbc_retail(),
        **bns_retail(),
        **tangerine_retail(),
        **icici_retail(),
        **manulife_retail(),
        **nbc_retail(),
        **simplii_retail(),
        **hsbc_retail(),
        **cdntire_retail(),
        **meridian_retail(),
        **eqbank_retail(),
        **wealthsimple_retail(),
        **laurentianbank_retail(),
        **motusbank_retail(),
        **motivefinancial_retail(),
        **duca_retail()
    }
    return merged_rates


def main():
    print(merged_retail_rates())


if __name__ == "__main__":
    main()
