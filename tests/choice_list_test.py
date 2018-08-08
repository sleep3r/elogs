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

red_button = browser.find_by_css("body > div.container.body > div > div.right_col > div.content > div.table > div > div.shift-mode-buttons > a:nth-child(2)").first.click()

if browser.is_element_present_by_css("body > div.jconfirm.jconfirm-supervan.jconfirm-open > div.jconfirm-scrollpane > div > div > div > div > div > div > div > div.jconfirm-buttons > button:nth-child(1)"):
    confirm_button = browser.find_by_css("body > div.jconfirm.jconfirm-supervan.jconfirm-open > div.jconfirm-scrollpane > div > div > div > div > div > div > div > div.jconfirm-buttons > button:nth-child(1)").first.click()
else:
    print("You're already in")


if browser.is_element_present_by_xpath('//*[@id="4843-big_table-conc_num-0"]'):
    print("All ok you idiot")

    #list_conc.select("ЗГОК")
else:
    print("lol")
