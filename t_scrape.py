import requests
import re
import xlsxwriter
from bs4 import BeautifulSoup
import os

# The list of all potential FI's websites that we might visit
pages = ["https://www.cibc.com/en/special-offers/fall-savings-promotion.html",
         "https://www.scotiabank.com/ca/en/personal/rates-prices/savings-account-rates.html",
         # "https://www.scotiabank.com/ca/en/personal/bank-accounts/savings-accounts/momentum-plus-savings-account.html",
         "https://www.tangerine.ca/en/landing-page/raptors"]

bank_list = {}

# Create our Excel output
workbook = xlsxwriter.Workbook('myoutput.xlsx')
worksheet = workbook.add_worksheet()

myheaders = ['Bank', 'Account Name', 'Details', 'Special Offer(s)']

for i, header in enumerate(myheaders):
    worksheet.write(1, i + 1, header)

for i, link in enumerate(pages):

    if link == "https://www.scotiabank.com/ca/en/personal/rates-prices/savings-account-rates.html":
        worksheet.write(i + 1, i, "Scotiabank")
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')

        scotia_momentum = {}

        # Finding Account name
        account_name = soup.find(class_='heading').text.strip()
        worksheet.write(i + 1, i + 1, account_name)

        # Finding Offer details
        detail = soup.find(class_='c--body').text.strip()
        worksheet.write(i + 1, i + 2, detail[0:53])

        perks = soup.find(class_='cmp cmp-text').find('p').text
        worksheet.write(i + 1, i + 3, perks)

        scotia_momentum["Bank"] = "Scotiabank"
        scotia_momentum["Account Name"] = account_name
        scotia_momentum["Details"] = detail
        scotia_momentum["Special Offer"] = perks

    elif link == "https://www.cibc.com/en/special-offers/fall-savings-promotion.html":
        worksheet.write(i + 3, i + 1, "CIBC")
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')

        cibc = {}

        account_name = soup.find(class_='rte longformtext base parbase').text.strip()
        worksheet.write(i + 3, i + 2, account_name[101:133])

        detail = soup.find(class_='rte longformtext base parbase').text.strip()
        worksheet.write(i + 3, i + 3, detail[0:36])

        perks = soup.find('span', class_='no-wrap').text.strip()
        perks2 = soup.find('span', class_='body-copy').text.strip()
        worksheet.write(i + 3, i + 4, perks)

        cibc["Bank"] = "Scotiabank"
        cibc["Account Name"] = account_name
        cibc["Details"] = detail
        cibc["Special Offer"] = perks

    elif link == "https://www.tangerine.ca/en/landing-page/raptors":
        worksheet.write(i + 2, i-1, "Tangerine")
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')

        tangerine = {}

        account_name = soup.find(class_='tngHeading-2 margin_top-60px margin_bottom-30px').text.strip()
        worksheet.write(i + 2, i, account_name[34:59])

        detail = soup.find(class_='tngHeading-2 margin_top-60px margin_bottom-30px').text.strip()
        worksheet.write(i + 2, i+1, detail)

        perks = soup.find(class_='tngBodyBase-prx').text.strip()
        worksheet.write(i+2, i+2, perks)



workbook.close()
