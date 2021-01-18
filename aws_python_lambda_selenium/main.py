import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def googleTesting():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/local/bin/chromedriver.exe")
    browser.get("http://www.google.com")

    txt = browser.find_element_by_css_selector('input.gNO89b').get_attribute('value')

    browser.close()

    return txt

def lambda_handler(event, context):
    result = googleTesting()
    return result