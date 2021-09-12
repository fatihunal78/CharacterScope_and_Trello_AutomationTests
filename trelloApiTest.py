import json
import unittest
import requests
from trello import *

import time
from selenium import webdriver
from selenium.webdriver import ActionChains

#pre-defined parameters
KEY = "836682262a6e7339f61e6d60791a9810"
TOKEN = "ead227704687b377ba549a6f6898339589a9f545a1c679f0bf05de0a32505755"
CHROME_DRIVER_PATH= r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'
USERNAME="fatihunal@gmail.com"
PASSWORD="FatihUnal123"

#board creation function
def create_board(board_name):
    url = "https://api.trello.com/1/boards/"
    querystring = {"name": board_name, "key": KEY, "token": TOKEN}
    response = requests.request("POST", url, params=querystring)
    board_id = response.json()["shortUrl"].split("/")[-1].strip()
    return board_id

#board deletion function
def delete_board(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}"
    querystring = {"key": KEY, "token": TOKEN}
    response = requests.request("DELETE", url, params=querystring)

#list creation function, it is necessary to create cards
def create_list(board_id, list_name):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    querystring = {"name": list_name, "key": KEY, "token": TOKEN}
    response = requests.request("POST", url, params=querystring)
    list_id = response.json()["id"]
    return list_id

#card creation function
def create_card(list_id, card_name):
    url = "https://api.trello.com/1/cards"
    querystring = {"name": card_name, "idList": list_id, "key": KEY, "token": TOKEN}
    response = requests.request("POST", url, params=querystring)
    card_id = response.json()["id"]
    return card_id

#card update function
def update_card(existing_card_id, new_card_name):
    url = f"https://api.trello.com/1/cards/{existing_card_id}"
    querystring = {"name": new_card_name, "key": KEY, "token": TOKEN}
    response = requests.request("PUT", url, params=querystring)

#card deletion function
def delete_card(existing_card_id):
    url = f"https://api.trello.com/1/cards/{existing_card_id}"
    querystring = {"key": KEY, "token": TOKEN}
    response = requests.request("DELETE", url, params=querystring)

#comment adding function to card
def add_comment(existing_card_id, comment):
    url = f"https://api.trello.com/1/cards/{existing_card_id}/actions/comments"
    querystring = {"key": KEY, "token": TOKEN, "text": comment}
    response = requests.request("POST", url, params=querystring)
    #print(response.text)

#function to obtain URL of board
def board_url(existing_board_id):
    url = f"https://api.trello.com/1/boards/{existing_board_id}"
    querystring = {"key": KEY, "token": TOKEN}
    response = requests.request("GET", url, params=querystring)
    return response.json()["url"]



if __name__ == '__main__':
    #creating a board
    myBoardId = create_board("myBoard")
    #adding a list name in the board
    myListId = create_list(myBoardId, "myToDoList")

    #creating three cards on that board
    myCardId1 = create_card(myListId, "myCard1")
    myCardId2 = create_card(myListId, "myCard2")
    myCardId3 = create_card(myListId, "myCard3")

    #editing name of one of the cards
    update_card(myCardId2, "myCard2 updated")

    #deleting one of the cards
    delete_card(myCardId1)

    #adding a comment to one of the cards
    add_comment(myCardId3, "This is first comment")

    #chrome driver
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    time.sleep(3)

    #trello login, entering username and password
    driver.get('https://trello.com/login')
    time.sleep(3)
    driver.find_element_by_xpath('//input[@id="user"]').send_keys(USERNAME)
    time.sleep(3)
    driver.find_element_by_xpath('//input[@id="login"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//input[@id="password"]').send_keys(PASSWORD)
    time.sleep(3)
    driver.find_element_by_xpath('//button[@id="login-submit"]').click()
    time.sleep(3)

    #directly opening the URL of the created board
    driver.get(board_url(myBoardId))
    time.sleep(2)

    #verifying that there are two cards on the board
    cardElements = driver.find_elements_by_xpath('//div[@id="board"]//a[starts-with(@class,"list-card ")]')
    assert (len(cardElements)==2), "There are not two Cards"

    #verifying that there is a card with a comment
    commentedCard = driver.find_elements_by_xpath('//div[@class="badge"][@title="Comments"]')
    assert (len(commentedCard) == 1), "There is not one Commented Card"

    #clicking the commented card
    iframe=driver.find_element_by_xpath('//div[@class="badge"][@title="Comments"]').click()
    time.sleep(2)

    #adding a new comment to that card
    driver.switch_to.frame(iframe)
    driver.find_element_by_xpath('//div[@class="new-comment js-new-comment mod-card-back"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//textarea[@class="comment-box-input js-new-comment-input"]').send_keys("This is second comment")
    driver.find_element_by_xpath('//input[@class="nch-button nch-button--primary confirm mod-no-top-bottom-margin js-add-comment"]').click()
    time.sleep(2)  

    #closing the pop-up window and returning to main board menu
    driver.find_element_by_xpath('//a[@class="icon-md icon-close dialog-close-button js-close-window"]').click()
    time.sleep(2)
    driver.switch_to.default_content()
    time.sleep(2)


    #Seting the commented card as done
    actionChains = ActionChains(driver)
    actionChains.drag_and_drop(driver.find_element_by_xpath('//div[@class="badge"][@title="Comments"]'), driver.find_element_by_xpath('//div[@class="list-header js-list-header u-clearfix is-menu-shown"]//textarea[@aria-label="Done"]')).perform()

    #As the number of boards to be created is limited, I delete the board that I have created after a while
    time.sleep(15)
    delete_board(myBoardId)


