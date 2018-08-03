from splinter import Browser

browser = Browser("chrome")
# сделать скриншот
screen_num = 0
def screen():
    global screen_num
    browser.driver.save_screenshot(f"screens/screenshot_all_ok_{screen_num}.png")
    screen_num += 1


# Режим редактирования
def pick_edit_mode():
    browser.find_by_css("body > div.container.body > div > div.right_col > div.content > div.table > div > div.shift-mode-buttons > a:nth-child(2)").first.click()


def edit_mode_confirm():
    if browser.is_element_present_by_css("body > div.jconfirm.jconfirm-supervan.jconfirm-open > div.jconfirm-scrollpane > div > div > div > div > div > div > div > div.jconfirm-buttons > button:nth-child(1)"):
        confirm_button = browser.find_by_css("body > div.jconfirm.jconfirm-supervan.jconfirm-open > div.jconfirm-scrollpane > div > div > div > div > div > div > div > div.jconfirm-buttons > button:nth-child(1)").first.click()
    else:
        print("You're already in")


# Режим валидации
def pick_val_mode():
    if browser.is_element_present_by_css("body > div.container.body > div > div.right_col > div.content > div.table > div > div.shift-mode-buttons > a:nth-child(3)"):
        browser.find_by_css("body > div.container.body > div > div.right_col > div.content > div.table > div > div.shift-mode-buttons > a:nth-child(3)").first.click()
    else:
        print("No reasons dude, you're already in")


# Комментарии к таблице
def comment_table_button():
    browser.find_by_css('#table_id_big_table > div.x_content > form > div:nth-child(4) > span').first.click()


def comment_table_field_fill():
    comment_field = browser.find_by_css('#table_id_big_table > div.x_content > form > div:nth-child(4) > div > textarea')
    comment_field.fill('Еблан, ты уволен!')


# Режим просмотра
def pick_view_mode():
    if browser.is_element_present_by_css('body > div.container.body > div > div.right_col > div.content > div.table > div > div.shift-mode-buttons > a:nth-child(1)',2):
        browser.find_by_css('body > div.container.body > div > div.right_col > div.content > div.table > div > div.shift-mode-buttons > a:nth-child(1)').first.click()
    else:
        print("You're here eblan")