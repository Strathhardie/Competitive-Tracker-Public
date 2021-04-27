from yaml_utils import YAMLUtils
import requests
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import time
import xlsxwriter
import pandas as pd
from lxml import html

#Function to write to workbook using xlsxwriter library
def writeWorkbook(overall_dict):
    #Create workbook and add sheet
    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()

    # Add title to top of Worksheet
    bold = workbook.add_format({'bold': True})
    worksheet.write('C1', 'Special Offers Scanner - Savings Accounts', bold)

    col = 1
    for x in overall_dict:
        # Write the name of the account in the 3rd row
        worksheet.write(3, col, x, bold)
        # Increase the width of columns B-D to 55 px
        worksheet.set_column('B:D', 55)
        # Incrase the height of row 4 to 80 px
        worksheet.set_row(4, 140)
        # Else write the detail in row 4 under respective column
        worksheet.write(4, col, overall_dict[x], bold)
        col = col + 1

    # Close workbook and remove sociabank rate image from pc
    workbook.close()

def main():
    banks = pd.read_csv('financial_institution_config.csv')

    # Create a progress bar
    #t = tqdm(banks, desc="Auditing Changes", leave=True, ncols=100, position=0)

    #Add headless option and open driver
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    
    #driver = webdriver.Chrome(chrome_options=chrome_options)


    #Initialize dictionary where key:value is BankName-AccountName:Offer
    offersDict = {}

    #for i in range (banks.shape[0]): 
    page = requests.get(banks.iloc[1, 2])
    tree = html.fromstring(page.content)

    offer = tree.xpath("h1 > span[class='subheading-medium'")
    print(offer)


main()