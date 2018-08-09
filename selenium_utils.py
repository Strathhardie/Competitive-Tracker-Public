# To install module, please enter command in terminal:
# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os


# This class contains all methods to handle selenium logic
class SeleniumUtils(object):

    # Returns the text given a url and xpath
    @staticmethod
    def getSourceXPathText(url, xpath):
        driver = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'resources/chromedriver.exe'))
        driver.get(url)
        return driver.find_element_by_xpath(xpath).get_attribute("innerHTML")

    # Saves the inner html of element to /websites directory
    # Sets encoding to utf-8 to avoid UnicodeEncodeError
    @staticmethod
    def saveSourceXPathText(url, xpath, pathToFile):
        with open (pathToFile, 'w', encoding="utf-8") as f:
            f.write(SeleniumUtils.getSourceXPathText(url, xpath))

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