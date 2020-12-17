from yaml_utils import YAMLUtils
from bs4 import BeautifulSoup as b
import requests
import json
from datetime import datetime
from selenium import webdriver
from tqdm import tqdm

"""
Makes various requests to bank websites and returns a dictionary containing special offers.

Args: 
    None

Returns:
    dict: a dict with keys of financial institutions and values representing special offers.
"""


def get_special_offers():
    bd = {}

    # CIBC
    soup = b(requests.get('https://www.cibc.com/en/special-offers/smart-fee-rebate.html').text, 'lxml')
    bd['CIBC'] = soup.find('span', class_='subheading-large-light').text + ";" + soup.find('span',
                                                                                           class_='banner-body-copy').text

    # RBC
    promos = requests.get('https://www.rbcroyalbank.com/accounts/_assets-custom/js/promo.json').json()
    bd['RBC'] = [x for x in set([(x["promo_name"] + "," + x["details"]) for x in promos.values()])]

    # BNS
    soup = b(requests.get(
        'https://www.scotiabank.com/ca/en/personal/bank-accounts/chequing-accounts/ultimate-package.html').text, 'lxml')
    bd['BNS'] = ''.join([x.text for x in soup.select('div[class="text-container stacked-container"] > div > p')])

    # TD

    soup = b(requests.get('https://www.td.com/ca/en/personal-banking/special-offers/300-chequing-offer/').text, 'lxml')
    bd['TD'] = soup.find('div', class_='td-col td-col-xs-12 td-col-sm-10 td-col-sm-offset-1').text + soup.find(
        'section', class_='td-text-with-link').text
    # BMO

    # todo requires selenium driver because of react

    # National Bank

    soup = b(requests.get('https://www.nbc.ca/personal/accounts/be-a-client.html').text, 'lxml')
    bd['NBC'] = soup.find('div', class_='col-xs-12 text-image-text-container').text

    # Simplii

    soup = b(requests.get('https://www.simplii.com/en/special-offers/no-fee-chequing-account.html').text, 'lxml')
    bd['SIMP'] = [x.text for x in
                  soup.select('div[class="nestedequalizer row"] > div > div[class="longformtext base parbase"]')]

    # Tangerine

    soup = b(requests.get('https://www.tangerine.ca/en/landing-page/special-offer/?ds_rl=1006592&gclsrc=aw.ds').text,
             'lxml')
    bd['TANG'] = [x.text for x in soup.find_all('h3', class_='body margin_bottom-10px')]

    # ICICI

    # todo

    # Manulife

    soup = b(
        requests.get('https://www.manulifebank.ca/personal-banking/bank-accounts/all-in-banking-package.html').text,
        'lxml')
    bd['MANU'] = soup.find('div',
                           "aem-GridColumn aem-GridColumn--default--8 aem-GridColumn--offset--default--2 aem-GridColumn--tablet--10 aem-GridColumn--offset--tablet--1 aem-GridColumn--phone--10 aem-GridColumn--offset--phone--1").h3.text

    # HSBC

    # todo

    # CDN Tire

    # todo

    # B2B Bank

    # todo

    # Merdian Credit

    # todo

    # EQ_Bank

    # todo

    return bd


"""
Makes various requests to bank websites and returns a dictionary containing special offers.

Args: 
    None

Returns:
    dict: a dict with keys of financial institutions and values representing special offers.
"""


def get_special_offer_accounts():
    # reading YAML File
    banks = YAMLUtils.readYAML("../" + YAMLUtils.FILE_NAME)

    # Create a progress bar
    t = tqdm(banks, desc="Auditing Changes", leave=True, ncols=100, position=0)

    try:
        # Selenium Driver initialization
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = True
        driver = webdriver.Firefox(options=fireFoxOptions)

        special_offers_dictionary = {}
        for index, bank in enumerate(banks):
            t.set_description("%-15s" % str(bank['name']))
            t.update()

            special_offers_dictionary[index] = {}

            special_offers_dictionary[index]['institution_name'] = bank['name']

            special_offers_dictionary[index]['accounts'] = []

            for account in bank['accounts']:
                driver.get(account['url'])

                soup = b(driver.page_source, 'html5lib')

                account_dictionary = {}
                account_dictionary['account_category'] = account['account_category']
                for k, v in account['elements'].items():
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
    print(get_special_offer_accounts())


main()
