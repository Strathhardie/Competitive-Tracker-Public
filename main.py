from yaml_utils import YAMLUtils
from selenium_utils import SeleniumUtils

def main():
    banks = YAMLUtils.readYAML(YAMLUtils.FILE_NAME)
    for bank in banks:
        # 1. Compare the previous xpath text (prevSrc) to the current xpath text (currSrc) of each bank
        f = open('websites/' + bank['name'] + ".txt", "r", encoding='utf-8')
        prevSrc = f.read()
        currSrc = SeleniumUtils.getSourceXPathText(bank['url'], bank['xpath'])

        # 2. Output whether the current xpath text has changed from the previous xpath text
        if (prevSrc == currSrc):
            print("No change in " + bank['name'] + "'s website")
        else:
            print("Change in " + bank['name'] + "'s website")

    # 3. Download the xpath text source for each bank, for the next run in the future (needs user input to re-download)
    usr_input = input('\nDo you want to download today\'s site for the next run? (y/n)')
    if(usr_input == 'y'):
        for bank in banks:
            SeleniumUtils.saveSourceXPathText(bank['url'], bank['xpath'], 'websites/' + bank['name'] + ".txt")
            # SeleniumUtils.saveSourceHTML(bank['url'], 'websites/' + bank['name'] + ".html")

main()