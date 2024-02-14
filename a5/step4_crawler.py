#!/usr/bin/env python
import queue
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
import time
# create a profile that disables caching
profile = FirefoxProfile()
profile.set_preference('browser.cache.disk.enable', False)
profile.set_preference('browser.cache.memory.enable', False)
profile.set_preference('browser.cache.offline.enable', False)
profile.set_preference('network.cookie.cookieBehavior', 2)

# open geckodriver with that profile and get our class webpage
browser = webdriver.Firefox(firefox_profile=profile)

first_page = 'https://computersecurityclass.com/4645316182537493008.html'

q = []
visited = set()
q.append(first_page)
page_ordering = []
i = 1
while len(q) > 0:
    cur_page = q.pop(0)
    browser.get(cur_page)
    time.sleep(7)
    cur_elements = browser.find_elements(By.XPATH, "//a[@href]")
    for cur_element in cur_elements:
        url = cur_element.get_attribute("href")
        if url not in visited and url not in q and url != cur_page:
            q.append(url)
    visited.add(cur_page)
    page_ordering.append(cur_page)
    i += 1


# close the page and quit the browser fully
browser.close()
browser.quit()

new_file = open('test.txt', "a")
for i in page_ordering:
    new_file.write(i + '\n')
