from yaml_utils import YAMLUtils
from selenium_utils import SeleniumUtils

def main():

    # 1. Compare the previous html to the current html of each bank

    # 2. Output whether the current html has changed from the previous html

    # 3. Download the HTML source for each bank, for the next run in the future
    banks = YAMLUtils.readYAML(YAMLUtils.FILE_NAME)
    for bank in banks:
        # Download the html source for each website
        SeleniumUtils.saveSourceHTML(bank['url'], 'websites/' + bank['name'] + ".html")
        
main()