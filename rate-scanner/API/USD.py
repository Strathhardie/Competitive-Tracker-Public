from bs4 import BeautifulSoup
import requests
import re
import json

#ToDo: Unit test cases for raw scraping, using table text or webpage text

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

'CUPA': CIBC - USD Personal Account
'CHISAUS': CIBC - Renaissance High Interest Savings Account (USD)

'''

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

    rates = {'CUPA': [0] * 11}
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
            for i in range(8, 11):
                rates["CUPA"][i] = float(rate[3])

    return rates


def cibc_broker_usd():
    url = 'https://www.renaissanceinvestments.ca/products/hisa'
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll("div", {"class": "hisa_rate"})[1].text
    rates = {}
    rates["CHISAUS"] = [float(re.findall('\d*\.?\d+', raw_data)[0])] * 11
    return rates


def td_usd():
    url = "https://www.td.com/ca/en/personal-banking/products/bank-accounts/account-rates/"
    response = requests.request("GET", url)

    soup = BeautifulSoup(response.text, features="html.parser")
    tables = soup.findAll("table")

    rates = {'TDUSD': [0] * 11}
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

    for i in range(8, 11):
        rates["TDUSD"][i] = raw_rates[7]

    return rates


def td_broker_usd():
    url = "https://www.td.com/ca/en/asset-management/additional-solutions/"
    response = requests.request("GET", url)

    soup = BeautifulSoup(response.text, features="html.parser")
    raw_rate = soup.findAll("table")[0].find_all('tr')[2].text

    #Regex pulls out any float value before a % sign
    rates = {'TDUSIS': [float(re.findall('\d*\.?\d+%', raw_rate)[0][:-1])] * 11}
    return rates


def rbc_usd():
    url = "https://apps.royalbank.com/apps/app-services/public-rates/api/publicrates"
    response = requests.request("GET", url)
    raw_rates = json.loads(response.text)['result_content']

    rates = {'RUSHIS': None, 'RUSPA ': None, 'RUSISA': None}

    # RUSHIS
    for rate in raw_rates:
        if rate['Name'] == '0206850001':
            rates["RUSHIS"] = [float(rate['Value'])]*11
    # RUSPA
    for rate in raw_rates:
        if rate['Name'] == '0007170002':
            rates["RUSPA"] = [float(rate['Value'])]*11

    # RUSISA
    # Series A USD
    for rate in raw_rates:
        if rate['Name'] == '0273740002':
            rates["RUSISA"] = [float(rate['Value'])]*11

    return rates


def bmo_usd():
    url = "https://www.bmo.com/bmocda/templates/json_bankacct_include.jsp"
    response = requests.request("GET", url)
    # parses js vars into a list of valid json objects
    regex = r"var (([\S]+)([^;]+))"
    raw_data = re.findall(regex, response.text.replace('\'', '"').replace('\\x', 'x'))
    raw_rates = {match[1]: json.loads(match[2].lstrip('= ')) for match in raw_data}

    rates = {'BPRSA_US': [0] * 11}

    for i in range(8):
        rates["BPRSA_US"][i] = float(raw_rates["PRSA_US"]["59999.99"]["value"])
    for i in range(8,11):
        rates["BPRSA_US"][i] = float(raw_rates["PRSA_US"]["99999999.99"]["value"])

    return rates


def bns_usd():
    url = "https://dmtsms.scotiabank.com/api/rates/daily/nonspecialaccountnew"
    response = requests.request("GET", url)
    raw_data = json.loads(response.text)
    rates = {"BNSUSDIA": [0] * 11}

    for data in raw_data["data"]:
        if data["PRODUCT"] == "U.S. DOLLAR DAILY INTEREST":
            for i in range(2):
                rates["BNSUSDIA"][i] = data["TERMS"][0]['RATE']
            for i in range(2, 4):
                rates["BNSUSDIA"][i] = data["TERMS"][1]['RATE']
            rates["BNSUSDIA"][4] = data["TERMS"][2]['RATE']
            for i in range(5, 11):
                rates["BNSUSDIA"][i] = data["TERMS"][3]['RATE']

    return rates

#ToDo
def bns_broker_usd():
    return {"BNSUSISA": [0]*11}


def tangerine_usd():
    # Mappings: https://www.tangerine.ca/static_files/Tangerine_FBE/WebAssets/js/historical-rates.js
    import xml.etree.ElementTree as ET
    import datetime
    url = "https://www.tangerine.ca/historicalrates/RatesHistory.xml"
    response = requests.request("GET", url)
    rate = sorted(ET.fromstring(response.text).findall('.//product[@type="3010"][@currency="USD"]/rate'),
                  key=lambda x: datetime.datetime.strptime(x[0].text, '%m/%d/%Y'), reverse=True)[0]
    return {'TUSSAV': [float(re.findall('\d*\.?\d+', rate[1].attrib['en'][:-1])[0])] * 11}


def icici_usd():
    url = "https://www.icicibank.ca/personal/hisave.page"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll("div", {"class": "rows clearfix"})[0].find_all("li")[1].text
    return {"ICUSHIS": [float(re.findall('\d*\.?\d+%', raw_data)[0][:-1])] * 11}


def manulife_usd():
    url = "https://www.manulifebank.ca/bin/mbank/manulifeglobalrates.json"
    response = requests.request("GET", url)
    raw_data = json.loads(response.text)
    return {"MUSAA": [float(raw_data['rateUSADVA_0'])] * 11, "MUSISA": [float(raw_data['rateUSISA_0'])] * 11}


def hsbc_usd():
    url = "https://www.hsbc.ca/savings-accounts/rates/"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    rates = {"HUSHRS": [0] * 11}

    raw_data = ''.join([tr.find_all("td")[0].text for tr in soup.findAll("table")[4].find_all("tr")[1:]])
    raw_rates = re.findall('\d*\.?\d+', raw_data)
    raw_rates = [float(i) for i in raw_rates]

    for i in range(6):
        rates["HUSHRS"][i] = raw_rates[0]
    rates["HUSHRS"][6] = raw_rates[1]
    for i in range(7, 9):
        rates["HUSHRS"][i] = raw_rates[2]
    for i in range(9, 11):
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
    return {"AUSCPA": [raw_rate]*11}


def scotia_broker():
    url = "https://www.scotiaitrade.com/en/direct-investing-and-online-trading/trading-fees/commissions-and-fees.html"
    response = requests.request("GET", url)

    soup = BeautifulSoup(response.text, features="html.parser")
    raw_data = soup.findAll("table")[3].find_all('td')[2].text
    return {"SCOUSA": [float(re.findall('\d*\.?\d+%', raw_data)[0][:-1])]*11 }


# ToDo: Exception handling, If module fails then recall.
def merged_usd_rates():
    merged_rates = {**cibc_usd(),
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
                    **scotia_broker()}

    return merged_rates

def main():
    print(merged_usd_rates())


if __name__ == "__main__":
    main()