from yaml_utils import YAMLUtils
from selenium_utils import SeleniumUtils
from parser_utils import ParserUtils
import datetime
import os

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
            bankData['websites/' + bank['name'] + '-' + account['account_name'] + '-' + dt + ".html"] = account['xpath']
        # Save the obtained HTML to the filepath

        # 2. Compare the downloaded html to the most recent previous html with the same account type and financial institution
        SeleniumUtils.saveBankAccountsXPathHTML(bank['url'], bankData)
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

main()