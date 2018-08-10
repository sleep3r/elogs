from splinter import Browser
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--log-level=3')

# driver = webdriver.Chrome("C:/Chromedriver/chromedriver.exe")
browser = Browser("chrome")
browser.visit("http://88.99.2.149:1337/furnace/fractional")
if browser.is_element_present_by_id("loginform", 2):
    browser.fill("username", "inframine")
    browser.fill("password", "Singapore2017")
    browser.find_by_css("input.btn").click()

button = browser.find_by_text("Добавить измерение").first.click()

button = browser.find_by_css("#modals-container > div > div > div.v--modal-box.v--modal > div > table:nth-child(3) > tr:nth-child(1) > td:nth-child(2) > i.glyphicon.glyphicon-plus").first.click()

if browser.is_element_present_by_css("#modals-container > div > div > div.v--modal-box.v--modal > div > table:nth-child(3) > tr:nth-child(1) > td:nth-child(2) > input[type='number']"):
    o_field_fr_1 =  browser.find_by_css("#modals-container > div > div > div.v--modal-box.v--modal > div > table:nth-child(3) > tr:nth-child(1) > td:nth-child(2) > input[type='number']")
    o_field_fr_1.fill("1")

if browser.is_element_present_by_css("#modals-container > div > div > div.v--modal-box.v--modal > div > table:nth-child(3) > tr:nth-child(2) > td:nth-child(2) > input[type='number']"):
    o_field_m_1 = browser.find_by_css("#modals-container > div > div > div.v--modal-box.v--modal > div > table:nth-child(3) > tr:nth-child(2) > td:nth-child(2) > input[type='number']")
    o_field_m_1.fill("1")

button = browser.find_by_css("#modals-container > div > div > div.v--modal-box.v--modal > div > div > button:nth-child(1)").first.click()

if browser.is_element_present_by_css("body > div.container.body > div > div.right_col > div:nth-child(2) > div:nth-child(1) > div > div.x_panel > div.x_content > div.carousel"):
    print("All ok")
else:
    print("Обжиг->Ситовой->Огарок/шихта SMTH wrong")

browser.quit()
