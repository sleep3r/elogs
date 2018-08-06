from splinter import Browser
from selenium import webdriver
import time
from utils.tools import *

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--log-level=3')

host = "http://88.99.2.149:"
port = "4242"
url = host + port

# browser = Browser("chrome")
browser.visit(f"{url}/furnace/concentrate_report_journal")
if browser.is_element_present_by_id("loginform", 2):
    browser.fill("username", "inframine")
    browser.fill("password", "Singapore2017")
    browser.find_by_css("input.btn").click()

pick_edit_mode()

edit_mode_confirm()

num_wag_field_1 = browser.find_by_css('.wagon_num_0')
num_wag_field_1.fill('22')
time.sleep(3)

pick_val_mode()

name_field = browser.find_by_css('.wagon_num_0')
name_field.click()


if browser.is_element_present_by_id('5505-big_table-wagon_num-0-comment'):
    print("zbs")
    val_comment_field = browser.find_by_css('#table_id_big_table > div.x_content > form > table > tbody > tr > td:nth-child(1) > span > textarea')
    val_comment_field.fill("WTF???")
else:
    print("fuck u")

time.sleep(3)

pick_edit_mode()

comment_table_button()
comment_table_field_fill()

time.sleep(3)

pick_view_mode()

comment_table_button()
