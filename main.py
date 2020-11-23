from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
import time
import random
from auth_data import username, password

class InstagramBot():

    # Set models
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome('chromedriver.exe')

    # Close browser
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    # Login to instagram account
    def login(self):
        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        try:
            accept_cookies = browser.find_element_by_xpath(
                "//button[contains(text(),'Accept')]")  # close 'Accept cookies'
            time.sleep(random.randrange(3, 5))
            accept_cookies.click()
            print('SUCCESS: Cookies closed')
        except:
            print('Cookies window not found')

        username_input = browser.find_element_by_name('username')  # input insta username
        username_input.clear()
        username_input.send_keys(username)
        time.sleep(random.randrange(3, 5))
        print('SUCCESS: Username inputed')

        password_input = browser.find_element_by_name('password')  # input insta password
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(random.randrange(3, 5))
        print('SUCCESS: Password inputed')

        password_input.send_keys(Keys.ENTER)
        time.sleep(random.randrange(3, 5))

        try:
            turn_off_notifications = browser.find_element_by_xpath(
                "//button[contains(text(),'Not Now')]")  # close notifications
            time.sleep(random.randrange(3, 5))
            turn_off_notifications.click()
            print('SUCCESS: Notifications window closed')
        except:
            print('Notification window not found')

    # Search posts by hashtag, saves all hashtegs to file, follow then and puts like to posts
    def like_photo_by_hashtag(self, hashtag):
        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/') # try to get page with posts which contains hashtags I need to put likes
        time.sleep(random.randrange(5, 10))
        print('SUCCESS: Hashtags window reached')

        for i in range(1, 4):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll page to get more posts, in this case scroll 4 times
            time.sleep(random.randrange(5, 8))

        hrefs = browser.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')] # save only posts links to this array

        for url in posts_urls: # Put like
            try:
                browser.get(url)
                time.sleep(10)
                like_button = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button')
                like_button.click()
                print(f'SUCCES: Like putted on {url}')
                time.sleep(random.randrange(80, 100))
            except:
                print(f'ERROR: Failed to put a like on {url}')
                self.close_browser()

    # Check if xpath to element exists
    def xpath_exists(self, url):
        browser = self.browser

        try:
            browser.find_element_by_xpath(url)
            exist = True
        except:
            exist = False

    # Like a specific post that he went to
    def put_exactly_like(self, userpost):
        browser = self.browser
        browser.get(userpost)
        time.sleep(random.randrange(5, 10))

        wrong_userpage = '/html/body/div[1]/section/main/div/h2'
        if self.xpath_exists(wrong_userpage):
            print('ERROR: This post does not exist')
            self.close_browser()
        else:
            print('SUCCESS: post found can be liked')
            time.sleep(random.randrange(3, 5))

            like_button = '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button'
            browser.find_element_by_xpath(like_button).click()
            time.sleep(random.randrange(3, 5))

            print(f'SUCCESS: post liked "{userpost}"')
            self.close_browser()

    # Put likes on many posts of instagram user
    def put_many_likes(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(random.randrange(3, 5))

        wrong_userpage = '/html/body/div[1]/section/main/div/h2'
        if self.xpath_exists(wrong_userpage):
            print('ERROR: This user does not exist')
            self.close_browser()
        else:
            print('SUCCESS: User found successfully, you can like it')
            time.sleep(random.randrange(3, 5))

            posts_count = int(browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text)
            loops_count = int(posts_count/12)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll page to get more posts
                time.sleep(random.randrange(3, 5))
                print(f'SUCCESS: Times scrolled {i}')

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            # Removes dublicated links
            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

            with open(f'{file_name}_set.txt') as file:
                urls_list = file.readlines()

                for post_url in urls_list:
                    try:
                        browser.get(post_url)
                        time.sleep(2)

                        like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                        browser.find_element_by_xpath(like_button).click()
                        time.sleep(random.randrange(80, 100))

                        print(f"SUCCESS: Like putted on {post_url}!")
                    except:
                        print(f'ERROR: Failed to put a like on {post_url}')
                        self.close_browser()

            # Remove files which was created
            # os.remove(f'{file_name}.txt')
            # os.remove(f'{file_name}_set.txt')

            self.close_browser()

mybot = InstagramBot(username, password)
mybot.login()
mybot.put_many_likes('https://www.instagram.com/lenabrand.official/')

















