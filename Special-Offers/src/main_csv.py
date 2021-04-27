import requests
import pandas as pd
import lxml.html
from bs4 import BeautifulSoup

def main():
    writer = StyleFrame.ExcelWriter('RateScanner.xlsx')

    default_style = Styler(font=utils.fonts.calibri)
    header_style = Styler(bold=True, font=utils.fonts.arial, font_size=10)
    
    
    df_banks = pd.read_csv('financial_institution_config.csv')
    print(df_banks)

    response = requests.get('https://www.cibc.com/en/special-offers/fall-savings-promotion.html')

main()