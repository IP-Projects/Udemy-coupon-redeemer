# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time

# maxPage = 1


def getNumberOfPages():
    maxPage = 0
    site = "https://onlinecourses.ooo"
    reqheaders = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    req = urllib.request.Request(site, headers=reqheaders)
    try:
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')

        data = soup.findAll('a', attrs={'class': 'page-numbers'})
        print(data)
        for pageNum in data:
            currentPage = pageNum.getText().replace(',', '').encode('ascii', 'ignore')
            if(currentPage != b''):
                print(currentPage)
                currentPage = int(currentPage)
                if maxPage < currentPage:
                    maxPage = currentPage
        print(maxPage)
    except:
        maxPage = 1
    return maxPage


def getLinks():
    maxPage = getNumberOfPages()
    for index in range(1, maxPage + 1):

        site = "https://onlinecourses.ooo/page/" + str(index) + '/'
        reqheaders = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        req = urllib.request.Request(site, headers=reqheaders)
        try:
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, 'html.parser')

            data = soup.findAll('h3', attrs={'class': 'entry-title'})
            for div in data:
                links = div.findAll('a')
                for a in links:
                    with open('index.txt', 'a') as fileWithLinks:
                        fileWithLinks.write(a['href']+'\n')
                        # print(a['href'])
        except:
            print("An exception occurred")


def getCouponLink():
    with open('index.txt') as fileWithLinks:
        siteList = fileWithLinks.readlines()
        siteList = [x.strip() for x in siteList]
    print(siteList)
    i = 1
    for site in siteList:
        print(i)
        i = i + 1
        reqheaders = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        req = urllib.request.Request(site, headers=reqheaders)
        try:
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, 'html.parser')

            data = soup.findAll('div', attrs={'class': 'link-holder'})
            for div in data:
                links = div.findAll('a')
                for a in links:
                    with open('couponFile.txt', 'a') as fileWithLinks:
                        fileWithLinks.write(a['href']+'\n')
                        # print(a['href'])
        except:
            print("An exception occurred")

# code running ok, but after 40 links a capcha is triggered


def redeemCoupons(username, password):
    with open('couponFile.txt') as fileWithLinks:
        siteList = fileWithLinks.readlines()
        siteList = [x.strip() for x in siteList]
    currentLink = 0
    # turn = 0

    options = webdriver.FirefoxOptions()
    options.firefox_binary = "./geckodriver.exe"
    driver = webdriver.Firefox(options=options)
    # driver.get("https://www.udemy.com/")
    driver.get("https://www.udemy.com/join/login-popup/")

    # try:
    #     time.sleep(random.randint(15, 30))
    #     getFormButton = driver.find_element_by_xpath(
    #         '/html/body/div[2]/div[1]/div[3]/div[4]/a')
    #     getFormButton.click()
    # except:
    #     pass

    time.sleep(random.randint(15, 40))

    attempt = 0
    succeded = False
    while succeded is False and attempt < 15:
        try:
            usernameInput = driver.find_element_by_xpath(
                f'//*[@id="email--{attempt}"]')
            succeded = True
        except:
            attempt += 1
    # print(usernameInput)
    passwordInput = driver.find_element_by_xpath('//*[@id="id_password"]')

    usernameInput.clear()
    usernameInput.send_keys(username)

    passwordInput.clear()
    passwordInput.send_keys(password)

    login = driver.find_element_by_xpath('//*[@id="submit-id-submit"]')
    login.click()

    for site in siteList:
        # if(currentLink >= 855):
            # if(currentLink % 15 == 0):
                # driver.quit()
                # if(turn == 1):
                    # driver = webdriver.Opera(options=options)
                    # turn = 0
                # else:
                #     driver = webdriver.Firefox()
                #     turn = 1

        # if(currentLink > 855):
        # used to open the link
        time.sleep(random.randint(20, 180))  # wait for the website to load
        driver.execute_script('window.open("' + site + '","_blank");')
        # switch the driver to the new page
        driver.switch_to.window(driver.window_handles[-1])
        try:
            time.sleep(random.randint(30, 60))  # wait for the website to load
            redeemButton = driver.find_element_by_xpath(
                '/html/body/div[2]/div[3]/div[5]/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div/div[5]/div/div/div/button')
            # print(redeemButton)
            redeemButton.click()
        except:
            print("already redeamed")
        time.sleep(random.randint(20, 30))
        driver.close()  # used to close the tab
        # used to switch back to the main tab
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(random.randint(20, 60))
        currentLink = currentLink + 1

    driver.quit()


# How to use, uncomment each function one by one, and input you username and password in the last one, in general 300 links are more than enough, a capcha will be triggered a lot earlier probably
# getLinks()
# getCouponLink()
redeemCoupons('<udemy username>', '<udemy password>')
