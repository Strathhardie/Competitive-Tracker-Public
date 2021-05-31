from yaml_utils import YAMLUtils
from bs4 import BeautifulSoup as bs
import requests
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# import chromedriver_binary  # Adds chromedriver binary to path
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import pandas as pd

def main(): 

    df = pd.read_csv("institution_config.csv")

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.simplii.com/en/bank-accounts/no-fee-chequing.html")
    element = driver.find_element_by_class_name('subheading-medium')
    print(element)

main()