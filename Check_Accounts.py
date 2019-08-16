from bs4 import BeautifulSoup
from selenium_utils import SeleniumUtils

pathTo = ""

def saveDataFiles(URL,pathTO):
 SeleniumUtils.saveSourceHTML(URL,r''+pathTO)


def findBankElements(bankName,pathTO,bankID,bankTable,NumberOfAccounts):

 with open(r'' + pathTO, "r", encoding="utf8") as f:
  page = f.read()
  soup = BeautifulSoup(page, 'html.parser')

  if bankName=="Simplii" or bankName=="RBC":
     divRowsbank = soup.find('div', id=bankID)
     Bankrows = divRowsbank.find_all(bankTable)
     if len(Bankrows) == len(NumberOfAccounts):
         print("No account has been added in the bank " + " " + bankName)
     elif len(Bankrows) > len(NumberOfAccounts):
         print(bankName + " " + "Bank account has been added")
     elif len(Bankrows) < len(NumberOfAccounts):
         print(bankName + " "+ NumberOfAccounts + " " + "Bank account has been deleted")

  elif bankName=="CIBC"  or bankName=="Scotiabank" or bankName=="BMO" or bankName=="ICICI" or bankName=="NBC":
   Bankrows = soup.find_all(bankTable)
   if len(Bankrows) == len(NumberOfAccounts):
       print("No account has been added in the bank"+ " " + bankName)
   elif len(Bankrows) > len(NumberOfAccounts):
      print(bankName + " " + "Bank account has been added." + " " + "Please add that particular account in the YAML file with account name and xpath under accounts node.")
   elif len(Bankrows) < len(NumberOfAccounts):
       print(bankName + " " + "Bank account has been deleted")