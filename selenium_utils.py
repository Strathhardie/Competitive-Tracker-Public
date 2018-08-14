# To install module, please enter command in terminal:
# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os


# This class contains all methods to handle selenium logic
class SeleniumUtils(object):

    # Returns the text given an xpath
    @staticmethod
    def getBankAccountXPathHTML(xpath, driver):
        return driver.find_element_by_xpath(xpath).get_attribute("innerHTML")

    # Creates the driver, and saves the obtained HTML from the xpath to the given file path
    @staticmethod
    def saveBankAccountsXPathHTML(url, bankData):
        driver = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'resources/chromedriver.exe'))
        driver.get(url)
        for filepath in bankData:
            with open(filepath, 'w', encoding="utf-8") as f:
                f.write(SeleniumUtils.getBankAccountXPathHTML(bankData[filepath], driver))

    # Returns the HTML source
    @staticmethod
    def getSourceHTML(url):
        driver = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'resources/chromedriver.exe'))
        driver.get(url)
        return driver.page_source

    # Saves the HTML source to /websites directory
    # Sets encoding to utf-8 to avoid UnicodeEncodeError
    @staticmethod
    def saveSourceHTML(url, pathToFile):
        with open (pathToFile, 'w', encoding="utf-8") as f:
            f.write(SeleniumUtils.getSourceHTML(url))

    '''
    # Method is just a demo
    @staticmethod
    def demo():
        driver = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'resources/chromedriver.exe'))
        driver.get("http://www.python.org")
        assert "Python" in driver.title
        elem = driver.find_element_by_name("q")
        elem.clear()
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        driver.close()
    '''