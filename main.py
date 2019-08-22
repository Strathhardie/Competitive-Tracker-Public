from yaml_utils import YAMLUtils
from selenium_utils import SeleniumUtils
from parser_utils import ParserUtils
import datetime
import os
from Check_Accounts import saveDataFiles
from Check_Accounts import findBankElements

def main():

    banks = YAMLUtils.readYAML(YAMLUtils.FILE_NAME)
    # 1. Save the current HTML with format <financial institution>-<account type>-<current date time>.html
    dt = '{:%Y%m%d_%H%M%S}'.format(datetime.datetime.now())
    # Iterate through each bank in the YAML

    for bank in banks:
        # Make a dictionary where key:value is filepath:xpath
        bankData = dict()
        # Go through each account in the bank
        for account in bank['accounts']:
          # Save each account's filepath, and the xpath to the dictionary

            if account['xpath'] == "none":
                print("")
            else:
             bankData['websites/' + bank['name'] + '-' + account['account_name'] + '-' + dt + ".html"] = account['xpath'];


        # Save the obtained HTML to the filepath
       # 2. Compare the downloaded html to the most recent previous html with the same account type and financial institution
        try:
            SeleniumUtils.saveBankAccountsXPathHTML(bank['url'], bankData)
        except(Exception) as error:
            print(error);
        for filepath in bankData:
            # Read the downloaded file contents, bank name, account, and datetime
            currSrcFile = open(filepath, encoding='utf-8')
            currSrc = currSrcFile.read()
            currSrcBankName = ParserUtils.parseBankName(filepath.split('/')[1])
            currSrcAccount = ParserUtils.parseAccount(filepath)
            currSrcDateTime = ParserUtils.parseDateTime(filepath)

            # Find the most recent previous file
            # Sort the files by reverse alphabetical order (most recent datetime first)
            files = sorted(os.listdir('websites'), reverse=True)
            for file in files:
                # If the bank name and account name are equal,
                # and the datetime is less than the current datetime, then it's the most recent.
                if (currSrcBankName == ParserUtils.parseBankName(file)
                        and currSrcAccount == ParserUtils.parseAccount(file)
                        and ParserUtils.dateTimeLessThan(ParserUtils.parseDateTime(file), currSrcDateTime)):
                    prevSrcFile = open('websites/' + file, encoding='utf-8')
                    prevSrc = prevSrcFile.read()
                    break
            # 3. Output whether the current xpath text has changed from the previous xpath text

            if (prevSrc == currSrc):
                print("No change in " + bank['name'] + "-" + currSrcAccount)
            else:
                print("Change detected in " + bank['name'] + "-" + currSrcAccount)

#        saveDataFiles(bank['url'],'WebsitesHTML/' + bank['name']  + '-' + dt + ".html")
#        findBankElements(bank['name'],'WebsitesHTML/' + bank['name']  + '-' + dt + ".html",bank['id'],bank['table'],bank['accounts'])


main()

