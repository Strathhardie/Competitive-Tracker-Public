from yaml_utils import YAMLUtils
from selenium_utils import SeleniumUtils
import datetime

def main():
    banks = YAMLUtils.readYAML(YAMLUtils.FILE_NAME)
    # Save current datetime
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
        SeleniumUtils.saveBankAccountsXPathHTML(bank['url'], bankData)
main()