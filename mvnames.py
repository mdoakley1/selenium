#!/usr/bin/python3

''' Script to  list all the "free" movies on Youtube's Movies & Shows" 

    Must download ChromeDriver from https://sites.google.com/a/chromium.org/chromedriver/downloads
    and save to /usr/local/bin (Linux) or C:\Windows (Windows).
'''

from selenium import webdriver
from selenium.webdriver.common.keys    import Keys
from selenium.webdriver.common.by      import By
from selenium.webdriver.support.ui     import WebDriverWait
from selenium.webdriver.support        import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import platform
import time

# Routine to scroll to the bottom of a page
def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def retrieve_movie_names():

    # Support running this script on linux and windows.
    CHROMEDRIVER_LINUX_PATH   = '/usr/local/bin/chromedriver'
    CHROMEDRIVER_WINDOWS_PATH = 'C:\\Windows\\chromedriver'
    
    PATH = CHROMEDRIVER_LINUX_PATH
    if platform.system() == 'Windows':
        PATH = CHROMEDRIVER_WINDOWS_PATH
    print('\nChrome Driver path = ', PATH)

    #Suppress meaningless "DevTools listening ..." diagnostic that appears on Windows
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(PATH, options=options)
    
    # If window width is too small, some needed html is not sent. Increase
    # width if necessary.
    window_size = driver.get_window_size()
    if window_size['width'] < 1800:
        driver.set_window_size(1800, window_size['height'])
        print('Adjusting window width so that we capture required fields')
    
    driver.get('https://www.youtube.com')

    link = driver.find_element_by_link_text("Movies & Shows")
    link.click()

    # Wait for "Free to watch" to become available, but don't click it
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Free to watch")))

    # Wait for "VIEW ALL" button to become available and click that
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "VIEW ALL")))
    element.click()

    # Scroll to bottom, wait a second for scrolling to complete. Both a local function (scroll_down) 
    # and a selenium operation (scrollingElement) are used. Sometimes the bottom is not reached.
    scroll_down(driver)
    driver.execute_script("var scrollingElement = \
        (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
    time.sleep(2)

    # All movie titles are in "span" elements with class name "style-scope ytd-grid-movie-renderer"
    spans = driver.find_elements_by_xpath('//span[@class="style-scope ytd-grid-movie-renderer"]')

    # Save all the title names to an array and sort it
    titles = []
    for s in spans:
        title = s.get_property('title')
        titles.append(title)

    titles.sort()
    cnt = 0
    for title in titles:
        cnt += 1
        print(f'{cnt:3}  ', title)

    print('\n# of movies: ', len(spans))

    # Close the browser window
    driver.quit()

if __name__ == "__main__":
    retrieve_movie_names()

exit()
