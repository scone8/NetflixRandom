from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import lxml.html as lh
import pandas
import getpass
import os

chromeOptions = webdriver.ChromeOptions()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

chromeOptions.add_argument("--disable-infobars")
'''prefs = {'profile.managed_default_content_settings.images':2}
chromeOptions.add_experimental_option("prefs", prefs)'''
driver = webdriver.Chrome(options=chromeOptions)

url='https://www.finder.com/ie/netflix-movies'
listOfMovies = pandas.read_html(url)
listOfMovies = listOfMovies[1].drop(['Year of release', 'Runtime (mins)'], 1)


def turnMovieOn(randomMovie):
    movieName = randomMovie.Title.to_string(index=False)
    movieName = movieName.lstrip(' ')
    #myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, '.searchTab')))
    driver.find_element_by_css_selector(".searchTab").click()
    search_input = driver.find_element_by_xpath('//input[@data-uia="search-box-input"]')
    search_input.send_keys(movieName)
    search_input.send_keys(Keys.ENTER)

    searchXPath = "//a[@aria-label='%s']"%movieName

    time.sleep(2)

    try:
        driver.find_element_by_xpath(searchXPath).click()
    except NoSuchElementException:
        time.sleep(3)
        driver.find_element_by_xpath('//a[aria-label="Netflix"]').click()
        getRandomMovie()

    driver.find_element_by_xpath('//span[text()="Play"]').click()
    input()

def getRandomMovie():
    randomMovie = listOfMovies.sample()
    print(randomMovie)
    turnMovieOn(randomMovie)

def login():
    driver.get('https://www.netflix.com/ie/login')

    email = input("Enter email: ")
    password = getpass.getpass(prompt="Password: ")

    email_input = driver.find_element_by_id("id_userLoginId")
    email_input.send_keys(email)

    password_input = driver.find_element_by_id("id_password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

    profile = input("Netflix Profile: ")

    time.sleep(3)

    driver.find_element_by_link_text(profile).click()

def main():
    login()
    getRandomMovie()
    driver.close()

if __name__ == "__main__":
    main()
