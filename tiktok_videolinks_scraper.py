"""
    Hi There -

We are looking for an automated solution, 
preferably in google sheets, in which we can enter a specific TikTok profile URL 
(example: https://www.tiktok.com/@charlidamelio) and retrieve back a list of the
video links associated with that profile (example: https://www.tiktok.com/@charlidamelio/video/6902086461508685062,
https://www.tiktok.com/@charlidamelio/video/6901927442085121285). 
"""


import requests
from agent import user_agent
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep


SCROLL_PAUSE_TIME = 0.5


driver = webdriver.Firefox(executable_path=r"G://GekoDriver//geckodriver.exe")
last_height = driver.execute_script("return document.body.scrollHeight")
driver.get('https://www.tiktok.com/@karinakross')

sleep(3)
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


n = 1
try:
    for _ in range(10000):
        print(driver.find_element_by_css_selector(
            f'div.jsx-2261688415:nth-child({n}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)').get_attribute('href'))
        n += 1
except NoSuchElementException as err:
    print('Done.')
