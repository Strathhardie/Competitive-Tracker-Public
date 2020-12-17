import requests
import re
import csv
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date

import pandas as pd
import os
from pathlib import Path
# pip install xlsxwriter
import xlsxwriter
import glob

#The list of all potential FI's websites that we might visit
pages = ["https://www.cibc.com/en/special-offers/fall-savings-promotion.html",
"https://www.scotiabank.com/ca/en/personal/rates-prices/savings-account-rates.html",
# "https://www.scotiabank.com/ca/en/personal/bank-accounts/savings-accounts/momentum-plus-savings-account.html",
"https://www.tangerine.ca/en/landing-page/raptors"]

#Today date in order to generate Excel timestamp
todayDate = str(date.today())

#This is write header to excel file
headers =['Bank','Account','Details','Special Offer']
book = Workbook()
sheet = book.active

for index, header in enumerate(headers):
    sheet.cell(row=1, column=index+1).value=header



for index, link in enumerate(pages):


    #SCO_MOME
    if link == "https://www.scotiabank.com/ca/en/personal/rates-prices/savings-account-rates.html":
        sheet.cell(row=index+2, column=1).value="Scotiabank"
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')

        #Account name
        account_name = soup.find(class_='heading').text.strip()
        sheet.cell(row=index+2, column=2).value=account_name

        # table = soup.find('div', class_ = '_momentum-plus-savings-rates')

        # #Offer detail
        # print(table.tbody)
        detail = soup.find('small').find('p').text.strip()
        # sheet.cell(row=index+2, column=3).value=detail

        perks = soup.find(class_='cmp cmp-text').find('p').text
        #sheet.cell(row=index+2, column=4).value=perks


    #CIBC
    elif link =="https://www.cibc.com/en/special-offers/fall-savings-promotion.html" :
        sheet.cell(row=index+2, column=1).value="CIBC"

        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')

        account_name= soup.find(text=re.compile('eAdvantage'))
        sheet.cell(row=index+2, column=2).value = account_name

        data = soup.find_all('div', class_ = 'longformtext base parbase')

        sheet.cell(row=index+2, column=3).value = data[4].text.strip()

        #Offer detail
        sheet.cell(row=index+2, column=4).value = data[3].text.strip()


    #Tangerine
    elif link =="https://www.tangerine.ca/en/landing-page/raptors" :
        sheet.cell(row=index+2, column=1).value="Tangerine"

        page= requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')

        #Account name
        account_name= soup.find(text=re.compile('Savings'))
        sheet.cell(row=index+2, column=2).value=account_name

        data = soup.find_all('div', class_ = 'tngFlex')

        #Offer 1
        offer1 = soup.find(class_ = 'tngWrapper').find('p').text.strip()
        sheet.cell(row=index+2, column=3).value = offer1

        #Offer 2
        sheet.cell(row=index+2, column=4).value = data[2].text.strip()

book.save("specialOffer"+todayDate+".xlsx")
####################################################




# def compare_changed_Special_Offer(previousFile,todayFile):



#Today date in order to generate Excel timestamp
todayDate = str(date.today())

#Get correct file
excelFile=glob.glob("specialOffer[0-9]*.xlsx")
excelFile = sorted(excelFile)
#path to files
currentDirectory = os.getcwd()+"\\"
path_OLD=Path(currentDirectory+excelFile[len(excelFile)-2])
path_NEW=Path(currentDirectory+excelFile[len(excelFile)-1])



# Read in the two excel files and fill NA
df_OLD = pd.read_excel(path_OLD,header=None, names=None).fillna(0)
df_NEW = pd.read_excel(path_NEW,header=None, names=None).fillna(0)


dfDiff = df_OLD.copy()
for row in range(dfDiff.shape[0]):
    for col in range(dfDiff.shape[1]):
        value_OLD = df_OLD.iloc[row,col]
        try:
            value_NEW = df_NEW.iloc[row,col]
            if value_OLD==value_NEW and value_NEW!=0:
                dfDiff.iloc[row,col] = df_NEW.iloc[row,col]
            elif value_OLD==value_NEW and value_NEW==0:
                dfDiff.iloc[row,col] = ""
            elif( value_OLD!=value_NEW and value_NEW==0):
                dfDiff.iloc[row,col] = ('Expired: {}').format(value_OLD)
            else:
                dfDiff.iloc[row,col] = ('Update: {}').format(value_NEW)

        except:
            dfDiff.iloc[row,col] = ('{}-->{}').format(value_OLD, 'NaN')
writer = pd.ExcelWriter("specialOffer_compare"+todayDate+".xlsx", engine='xlsxwriter') # pylint: disable=abstract-class-instantiated
dfDiff.to_excel(writer, sheet_name='DIFF', index=False, header=None)




workbook  = writer.book
worksheet = writer.sheets['DIFF']


# define formats
highlight_fmt_red = workbook.add_format({'font_color': '#000000', 'bg_color':'#FF0000'})
highlight_fmt_yellow = workbook.add_format({'font_color': '#000000', 'bg_color':'#FFFF00'})

## highlight Update cells
worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
                                        'criteria': 'containing',
                                        'value':'Update',
                                        'format': highlight_fmt_yellow})
## highlight Expired cells
worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
                                        'criteria': 'containing',
                                        'value':'Expired',
                                        'format': highlight_fmt_red})
# save
writer.save()