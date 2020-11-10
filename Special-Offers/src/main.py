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
    banks = YAMLUtils.readYAML("../xpath-"+YAMLUtils.FILE_NAME)

    # Create a progress bar
    t = tqdm(banks, desc="Auditing Changes", leave=True, ncols=100, position=0)

    #Add headless option and open driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)


    #Initialize dictionary where key:value is BankName-AccountName:Offer
    offersDict = {}

    for bank in t:
        #Change the description of the progress bar to the current bank's name
        t.set_description("%-15s" % str(bank['name']))
        t.update()

        driver.get(bank['url'])
        delay = 10
        bankName = bank['name']

        #Iterate through each account in the bank (Only 1 for now for testing purposes)
        for account in bank['accounts']:
            offer = ''
            xis = account['xpath'].split(",")
            accountName = account['account_name']
            for xpath in xis:
                try:
                    element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
                    offer = offer + element.text
                except TimeoutException:
                    tqdm.write("Page took too long to load.")

            offersDict[bankName+" - "+accountName] = offer

    writeWorkbook(offersDict)


main()