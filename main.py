from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

website = 'https://www.audible.com/search'
path = "/Users/firozfahim/Downloads/chromedriver-mac-arm64/chromedriver"

# Set up Chrome options
chrome_options = Options()

# Set up Chrome driver service
service = Service(executable_path=path)

# Initialize the Chrome driver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(website)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

#container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')

container = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container'))
)
products= container.find_elements(By.XPATH, './li[contains(@class, "productListItem")]')
print(f"Found {len(products)} products")

time.sleep(10)

book_title =[]
book_author= []
book_length =[]

for product in products:
    try:
        book_title.append(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
    except:
        book_title.append(None)
    try:
        book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
    except:
        book_author.append(None)
    try:
        book_length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)
    except:
        book_length.append(None)

driver.quit()
time.sleep(10)

df_books= pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv("BookData.csv", index=False)






