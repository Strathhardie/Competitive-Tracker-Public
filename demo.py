from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

driver = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'resources/chromedriver.exe'))
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
# testing merge conflicts!