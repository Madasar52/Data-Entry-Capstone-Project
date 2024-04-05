import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os




GOOGLE_FORMS_LINK = os.environ.get("google_forms_link")
ZILLOW_LINK_BS = os.environ.get("zillow_link")


response = requests.get(ZILLOW_LINK_BS)
webpage = response.text
soup = BeautifulSoup(webpage, 'html.parser')


# 1. getting rent prices
rent_prices = soup.select(selector='.PropertyCardWrapper__StyledPriceLine')
rent_price_list = []
for each_price in rent_prices:
    x = each_price.text.replace(",", '')
    x = x.replace("+", '')
    x = x.replace("/mo", '')
    x = x.replace("1 bd", '')
    x = x.replace('1bd', '')
    rent_price_list.append(x)

# 2. getting rent addresses
rent_addresses = soup.select(selector='address[data-test="property-card-addr"]')
rent_address_list = []
for address in rent_addresses:
    y = address.text.replace('\n', '')
    y = y.strip()
    rent_address_list.append(y)

# getting rent links
rent_links = soup.select(selector='.StyledPropertyCardDataWrapper a[data-test="property-card-link"]')
rent_link_list = [link.get("href") for link in rent_links]


# 3. filling google form with selenium



n = 0
for n in range(len(rent_address_list)):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(GOOGLE_FORMS_LINK)
    time.sleep(2)
    input_address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_address.send_keys(rent_address_list[n])
    input_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_price.send_keys(rent_price_list[n])
    input_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_link.send_keys(rent_link_list[n])
    submit = driver.find_element(By.CSS_SELECTOR, 'div[jsname="M2UYVd"]')
    submit.click()
    driver.quit()
    n += 1





































































