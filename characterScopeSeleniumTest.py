# Maximize view is tested on Desktop, by using Chrome.

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver import ActionChains

# pre-defined parameters for chrome driver path and characterscope user link
CHROME_DRIVER_PATH = r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'
CHARACTERSCOPE_USER_LINK = 'https://characterscope-qa.azurewebsites.net/test/login?currentSession=0&isFullMember=true&redirect=%2Fhome'


if __name__ == '__main__':

    #chrome driver
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    time.sleep(3)

    # Characterscope session page
    driver.get(CHARACTERSCOPE_USER_LINK)
    # timeout period
    timeout = 5

    # wait until page is loaded
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//div[@class="btn btn-primary btn-lg"]'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    # scrolling down till the end of page and clicking the link there
    element = driver.find_element_by_xpath("//*[contains(text(),'Click here for a secret')]")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    actions.click(element).perform()
    time.sleep(1)

    # scrolling up till the beginning of the page
    element = driver.find_element_by_xpath("//div[@class='btn btn-primary btn-lg']")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    time.sleep(1)

    # scrolling down till the end of page by using scroll function
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    time.sleep(1)
    # scrolling up till the start of page by using scroll function
    driver.execute_script("window.scroll(0, 0);")
    time.sleep(1)

    # scrolling up and down with keyboard keys
    actions = ActionChains(driver)
    actions.send_keys(Keys.END).perform()
    time.sleep(1)
    actions.send_keys(Keys.HOME).perform()
    time.sleep(1)

    # maximizing and minimizing the window
    driver.maximize_window()
    time.sleep(1)
    driver.minimize_window()
    time.sleep(1)
    driver.maximize_window()
    time.sleep(1)

    # Clicking on the "Go" button in order to pass to the next page
    element = driver.find_element_by_xpath("//div[@class='btn btn-primary btn-lg']")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    actions.click(element).perform()

    # Returning back to the previous page
    time.sleep(2)
    driver.back()
    time.sleep(2)

    # clicking on the image link in order to pass to the next page
    element = driver.find_element_by_xpath("//div[@class='session-tile tile-shadow']")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    actions.click(element).perform()

    # Returning back to the previous page
    time.sleep(2)
    driver.back()
    time.sleep(2)

    # Clicking to the button again
    element = driver.find_element_by_xpath("//div[@class='btn btn-primary btn-lg']")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    actions.click(element).perform()
    time.sleep(2)

    # trying to click every session
    driver.find_element_by_xpath('//div[@data-session-id="MappingYourStrengths"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//div[@data-session-id="SoloReport"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//div[@data-session-id="ViewpointsInvite"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//div[@data-session-id="ViewpointsReport"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//div[@data-session-id="Engage"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//div[@data-session-id="Develop"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//div[@data-session-id="MappingYourStrengths"]').click()
    time.sleep(1)

    # trying to turn the circle
    for i in range(6):
        # here drag and drop is applied on the circle in order to round it six times
        sourceEle = driver.find_element(By.XPATH, '//div[@class="circle-arcs visible-wide circle-arcs-6"]')
        targetEle = driver.find_element(By.XPATH, '//div[@class="selected-session-heading"]')
        actionChains = ActionChains(driver)
        actionChains.click_and_hold(sourceEle).drag_and_drop(sourceEle,targetEle).perform()
        time.sleep(2)

    driver.find_element_by_xpath('//div[@data-session-id="MappingYourStrengths"]').click()
    time.sleep(3)
    # Clicking "Start Session" button for mobile portrait view
    # driver.find_element_by_xpath('//div[@class="mobile-portrait-start-button-wrapper visible-mobile"]').click()

    # Clicking "Start Session" button for mobile landscape view
    # driver.find_element_by_xpath('//div[@class="mobile-landscape-start-button-wrapper visible-mobile"]').click()

    # Clicking "Start Session" button for desktop maximize view
    driver.find_element_by_xpath('//a[@class="btn btn-lg btn-primary"]').click()

    # Clicking "Start Session" button for desktop smaller view
    # driver.find_element_by_xpath('//a[@class="btn btn-primary btn-lg"]').click()

    # closing the pop-up page if exists
    if len(driver.find_elements_by_xpath('//div[@id="mixpanel-notification-cancel"]')) > 0:
        driver.find_element_by_xpath('//div[@id="mixpanel-notification-cancel"]').click()

    driver.switch_to.default_content()
    time.sleep(2)
