from splinter import Browser

browser = Browser("chrome")
browser.visit("http://127.0.0.1:8000/leaching/leaching_express_analysis")
if browser.is_element_present_by_id("loginform", 2):
    browser.fill("username", "inframine")
    browser.fill("password", "Singapore2017")
    browser.find_by_css("input.btn").click()

if browser.is_element_present_by_id("table_id_loads_table", 2):
    browser.driver.save_screenshot("screenshot.png")
    print("All OK")
else:
    browser.driver.save_screenshot("errors.png")
    print("Some wrong!")

browser.quit()
