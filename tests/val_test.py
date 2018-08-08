from splinter import Browser
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--log-level=3')

browser = Browser("chrome")
browser.visit("http://88.99.2.149:1337/furnace/concentrate_report_journal")
if browser.is_element_present_by_id("loginform", 2):
    browser.fill("username", "inframine")
    browser.fill("password", "Singapore2017")
    browser.find_by_css("input.btn").click()

#if browser.is_element_present_by_css("body > div.container.body > div > div.right_col > div.content > div.table > div > div.shift-mode-buttons > a:nth-child(3)"):
#    val_button = browser.find_by_css("body > div.container.body > div > div.right_col > div.content > div.table > div > div.shift-mode-buttons > a:nth-child(3)").first.click()
#else:
#    print("No reasons dude, you're already in")

name_field = browser.find_by_xpath('//*[@id="5233-upper_table-senior_crane_operator-0"]')
name_field.click()
comment_field = browser.find_by_xpath('//*[@id="5233-upper_table-senior_crane_operator-0-comment"]')
comment_field.fill("WTF???")
