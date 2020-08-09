from selenium import webdriver

def init():
    option = webdriver.ChromeOptions()
    option.add_argument("--user-data-dir=" + r"~/.config/google-chrome/")
    browser = webdriver.Chrome(chrome_options=option)
    return browser
