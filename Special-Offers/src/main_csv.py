import requests
import pandas as pd
import lxml.html
from bs4 import BeautifulSoup

def main():
    df_banks = pd.read_csv('financial_institution_config.csv')
    print(df_banks)

    response = requests.get('https://www.cibc.com/en/special-offers/fall-savings-promotion.html')

main()