# To install module, please enter command in terminal:
# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import time

# This class contains all methods to handle selenium logic
class SeleniumUtils(object):

    driver = None

    @classmethod
    def initializeDriver(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        SeleniumUtils.driver = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'resources/chromedriver.exe'), chrome_options=chrome_options)
        SeleniumUtils.driver.implicitly_wait(5)

    # Returns the text given an xpath
    @classmethod
    def getBankAccountXPathHTML(cls, xpath, driver):
        return driver.find_element_by_xpath(xpath).get_attribute("innerHTML")

    # Creates the driver, and saves the obtained HTML from the xpath to the given file path
    @classmethod
    def saveBankAccountXPathHTML(cls, url, filepath, bankData):
        SeleniumUtils.driver.get(url)
        time.sleep(0.5)
        with open(filepath, 'w', encoding="utf-8") as f:
            f.write(SeleniumUtils.getBankAccountXPathHTML(bankData[filepath], SeleniumUtils.driver))

    # Returns the HTML source
    @classmethod
    def getSourceHTML(cls, url):
        SeleniumUtils.driver.get(url)
        time.sleep(0.5)
        return SeleniumUtils.driver.page_source

    # Saves the HTML source to /websites directory
    # Sets encoding to utf-8 to avoid UnicodeEncodeError
    @classmethod
    def saveSourceHTML(cls, url, pathToFile):
        with open (pathToFile, 'w', encoding="UTF-8") as f:
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