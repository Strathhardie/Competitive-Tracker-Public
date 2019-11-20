from yaml_utils import YAMLUtils
from selenium_utils import SeleniumUtils
from parser_utils import ParserUtils
import logging_utils as LoggingUtils
import datetime
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def main():
    # Initialize a boolean to check if a change has been detected, to improve output display at the end of execution
    change_detected = False
    error_encountered = False
    banks = YAMLUtils.readYAML(YAMLUtils.FILE_NAME)
    # Create a progress bar to track the auditor at a bank level
    t = tqdm(banks, desc="Auditing Changes", leave=True, ncols=100, position=0)
    # Initialize the webdriver so we don't have to create a new instance of driver every time we change banks
    SeleniumUtils.initializeDriver()
    # Initialize the logger
    logger = LoggingUtils.initialize_logger()

    # 1. Save the current HTML with format <financial institution>-<account type>-<current date time>.html
    dt = '{:%Y%m%d_%H%M%S}'.format(datetime.datetime.now())
    
    logger.newline()

    # Iterate through each bank in the YAML
    for bank in t:  
        # Change the description of the progress bar to the current bank's name
        t.set_description("%-15s" % str(bank['name']))
        t.update()  
        # Make a dictionary where key:value is filepath:xpath
        bankData = dict()
        # Go through each account in the bank
        for account in bank['accounts']:
          # Save each account's filepath, and the xpath to the dictionary
            if account['xpath'] == "none":
                pass
            else:
                bankData['websites/' + bank['name'] + '-' + account['account_name'] + '-' + dt + ".html"] = account['xpath']
                
        # Save the obtained HTML to the filepath
        # 2. Compare the downloaded html to the most recent previous html with the same account type and financial institution
        for filepath in bankData:
            currSrcBankName = ParserUtils.parseBankName(filepath.split('/')[1])
            currSrcAccount = ParserUtils.parseAccount(filepath)
            currSrcDateTime = ParserUtils.parseDateTime(filepath)
            try:                
                SeleniumUtils.saveBankAccountXPathHTML(bank['url'], filepath, bankData) 
            except (TimeoutError) as timeOut:
                logger.error(bank['name'] + "--" + currSrcAccount + "--" + "Error in execution: TimeoutError")
                continue
            except(Exception) as error:
                tqdm.write(str(error))
                logger.error(bank['name'] + "--" + currSrcAccount + "--" + "Error in execution: Unable to locate element")
            else:           
                # Read the downloaded file contents, bank name, account, and datetime
                with open(filepath, encoding='utf-8') as currSrcFile: currSrc = currSrcFile.read()                
        
                # Find the most recent previous file
                # Sort the files by reverse alphabetical order (most recent datetime first)
                files = sorted(os.listdir('websites'), reverse=True)
                for file in files:
                    # If the bank name and account name are equal,
                    # and the datetime is less than the current datetime, then it's the most recent.
                    if (currSrcBankName == ParserUtils.parseBankName(file)
                            and currSrcAccount == ParserUtils.parseAccount(file)
                            and ParserUtils.dateTimeLessThan(ParserUtils.parseDateTime(file), currSrcDateTime)):
                        with open('websites/' + file, encoding='utf-8') as prevSrcFile: prevSrc = prevSrcFile.read()
                        break

                # 3. Log whether the current xpath text has changed from the previous xpath text
                if (prevSrc == currSrc):
                    logger.info(bank['name'] + "--" + currSrcAccount + "--" + "No change")
                    # if no change was made, delete the latest version
                    os.remove(filepath)
                else:
                    logger.warning(bank['name'] + "--" + currSrcAccount + "--" + "Change detected")
                    change_detected = True
        

        # 4. Count the number of accounts for a given banks to determine if one is added or removed
        # EQ bank is currently out of scope due to having only one bank account, not in a table
        if bank['name'] != 'EQ_Bank':
            path = 'full_websites/' + bank['name'] + '-' + dt + '.html'
            SeleniumUtils.saveSourceHTML(bank['url'], path)
            #check to see if file was properly retrived by measuring the size if file is below 2kb it will reload it again
            while os.path.getsize(path) < 2000:
                SeleniumUtils.saveSourceHTML(bank['url'], path)

            with open(path,encoding="utf-8") as f: data = f.read()
            global count; count = 0                     
            global soup; soup = BeautifulSoup(data, 'html.parser') 
            # Based on the functions in the yaml, search the HTML page for specific elements and count them       
            for fn in bank['functions']:
                command = 'count += str(' + fn['function'] + '(' + fn['param'] + ')' + fn['suffix'] + ').count(\'' + fn['count'] + '\')'
                exec(command, globals())
            # If the count is not equal to the original number of accounts, output message and update the yaml
            if count > bank['total_count']:
                logger.warning("Account(s) added to " + bank['name'])
                YAMLUtils.writeYAML(YAMLUtils.FILE_NAME, bank['name'], count)
                change_detected = True
                
            elif count < bank['total_count']:
                logger.warning("Account(s) removed from " + bank['name'])
                YAMLUtils.writeYAML(YAMLUtils.FILE_NAME, bank['name'], count)
                change_detected = True
            else:
                #If no change is detected it will delete the latest addition
                os.remove(path)            

    print("Change(s) detected." if change_detected else "No changes detected.", "Please refer to results.log for further details.") 
    if error_encountered: print("Error(s) encountered. Please refer to results.log for further details.")   
    

main()

