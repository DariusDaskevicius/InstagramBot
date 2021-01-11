from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import random
import requests
from auth_data import username, password, hashtags, min_posts, min_followers, max_posts, max_followers

class InstagramBot():

    # Set models
    def __init__(self, username, password, min_posts, min_followers, max_posts, max_followers):
        self.min_posts = min_posts
        self.min_followers = min_followers
        self.max_posts = max_posts
        self.max_followers = max_followers
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome('chromedriver.exe')

    # Close browser
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    # Check if xpath to element exists
    def xpath_exists(self, path):
        browser = self.browser

        try:
            browser.find_element_by_xpath(path)
            exist = True
        except:
            exist = False

        return exist

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
        time.sleep(random.randrange(5, 7))

        try:
            dont_save_password = browser.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div/div/button')
            time.sleep(random.randrange(3, 5))
            dont_save_password.click()
            print('SUCCESS: Save your password window window closed')
        except:
            print('Save your password window not found')
            time.sleep(random.randrange(3, 5))

        try:
            turn_off_notifications = browser.find_element_by_xpath(
                "//button[contains(text(),'Not Now')]")  # close notifications
            time.sleep(random.randrange(3, 5))
            turn_off_notifications.click()
            print('SUCCESS: Notifications window closed')
        except:
            print('Notification window not found')
            time.sleep(random.randrange(3, 5))

    def search_accounts(self, pages):
        browser = self.browser
        time.sleep(random.randrange(3, 5))

        for page in pages:
            current_hashtag = page

            current_urls = self.save_urls_by_hashtag(current_hashtag)
            time.sleep(random.randrange(3, 5))

            current_accounts = self.get_urls_to_accounts(current_urls)
            time.sleep(random.randrange(3, 5))

            self.scrap_accounts(current_accounts)
            time.sleep(random.randrange(3, 5))

    # Search posts by hashtag, saves all hashtags to file, follow then and puts like to posts
    def save_urls_by_hashtag(self, hashtag):
        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/') # try to get page with posts which contains hashtags I need to put likes
        time.sleep(random.randrange(3, 5))
        print('SUCCESS: Hashtags window reached')

        # scroll page to get more posts, in this case scroll 4 times
        for i in range(1, 5):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')] # save only posts links to this array
        set_posts_urls = set(posts_urls)
        set_posts_urls = list(set_posts_urls)
        return set_posts_urls

    def get_urls_to_accounts(self, post_urls):
        browser = self.browser
        current_urls_to_account = []

        for post_url in post_urls:
            browser.get(post_url) # try to get page with posts which contains hashtags I need to put likes
            time.sleep(random.randrange(3, 5))

            try:
                get_url_to_account = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a')
                get_url_to_account.get_attribute('href')

                print(get_url_to_account.text)

                with open('accounts_urls.txt', 'r') as file:
                    accounts = file.readlines()
                    for i in accounts:
                        if i == get_url_to_account:
                            print('CATCH: User was already scraped :)')
                        else:
                            print('SUCCESS: Link to user taken')
                            current_urls_to_account.append('https://www.instagram.com/' + get_url_to_account.text)
                            set_current_urls_to_account = set(current_urls_to_account)
                            set_current_urls_to_account = list(set_current_urls_to_account)
            except:
                pass

        with open('accounts_urls.txt', 'a') as file:
            for url in set_current_urls_to_account:
                file.write(url + '\n')

        return set_current_urls_to_account

    def scrap_accounts(self, pages):
        browser = self.browser
        min_posts = self.min_posts
        min_followers = self.min_followers
        max_posts = self.max_posts
        max_followers = self.max_followers

        for page in pages:
            browser.get(page)  # try to get page with posts which contains hashtags I need to put likes
            time.sleep(random.randrange(3, 5))

            wrong_userpage = ''
            closed_account = ''

            try:
                wrong_userpage = browser.find_element_by_xpath('/html/body/div[1]/section/main/div')
            except:
                pass
            try:
                closed_account = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[1]/div')
            except:
                pass
            
            if self.xpath_exists(wrong_userpage):
                print('ERROR: Wrong userpage')
            else:
                if self.xpath_exists(closed_account):
                    print("CATCH: Account is closed. Can't be scrapped")
                else:
                    try:
                        posts_count = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text
                        try:
                            followers_count = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span')
                        except:
                            pass
                        try:
                            followers_count = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/ul/li[2]/span/span')
                        except:
                            pass
                        followers = followers_count.text

                        valid_followers_count = 3
                        valid_posts_count = 3

                        try:
                            valid_followers_count = int(followers)
                        except:
                            pass
                        if '.' in followers:
                            followers = followers.replace('.', '')
                            try:
                                valid_followers_count = int(followers)
                            except:
                                pass
                        if ',' in followers:
                            followers = followers.replace(',', '')
                            try:
                                valid_followers_count = int(followers)
                            except:
                                pass
                        if 'k' in followers:
                            followers_string = followers.replace('k', '')
                            valid_followers_count = int(followers_string)
                            valid_followers_count = valid_followers_count * 1000
                        if 'm' in followers:
                            followers_string = followers.replace('m', '')
                            valid_followers_count = int(followers_string)
                            valid_followers_count = valid_followers_count * 1000000

                        try:
                            valid_posts_count = int(posts_count)
                        except:
                            pass
                        if '.' in posts_count:
                            posts = posts_count.replace('.', '')
                            valid_posts_count = int(posts)
                        if ',' in posts_count:
                            posts = posts_count.replace(',', '')
                            valid_posts_count = int(posts)


                        print(valid_posts_count)
                        print(valid_followers_count)

                        name = 'not_found'
                        if self.xpath_exists('/html/body/div[1]/section/main/div/header/section/div[1]/h1'):
                            name = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/h1').text
                        if self.xpath_exists('/html/body/div[1]/section/main/div/header/section/div[1]/h2'):
                            name = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/h2').text

                        if valid_posts_count > min_posts and valid_posts_count < max_posts and valid_followers_count > min_followers and valid_followers_count < max_followers:
                            for scroll in range(0, 4):
                                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll page to get more posts
                                time.sleep(random.randrange(3, 5))
                                hrefs = browser.find_elements_by_tag_name('a')
                                posts_urls = [item.get_attribute('href') for item in hrefs if'/p/' in item.get_attribute('href')]  # save only posts links to this array

                            set_posts_urls = set(posts_urls)
                            set_posts_urls = list(set_posts_urls)

                            self.get_images(set_posts_urls, name)
                    except:
                        pass

        for i in set_posts_urls:
            print(i)

        return set_posts_urls

    def get_images(self, posts, page):
        browser = self.browser
        img_src_urls = []

        for post in posts:
            browser.get(post)  # try to get page with posts which contains hashtags I need to put likes
            time.sleep(random.randrange(3, 5))
            image_src = ''

            if self.xpath_exists('/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img'):
                image_src = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img'
            if self.xpath_exists('/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img'):
                image_src = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img'
            if self.xpath_exists('/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/img'):
                image_src = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/img'
            if self.xpath_exists('/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div[1]/img'):
                image_src = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div[1]/img'

            post_id = post.split('/')[-2]

            try:
                if self.xpath_exists(image_src):
                    img_src_url = browser.find_element_by_xpath(image_src).get_attribute("src")
                    img_src_urls.append(img_src_url)

                    get_img = requests.get(img_src_url)
                    time.sleep(random.randrange(3, 5))

                    if os.path.exists(f'{page}'):
                        print('Folder exists')
                    else:
                        os.mkdir(page)

                    with open(f'{page}/{page}_{post_id}_img.jpg', 'wb') as img_file:
                        img_file.write(get_img.content)
                else:
                    print('Not a image')
            except:
                pass

mybot = InstagramBot(username, password, min_posts, min_followers, max_posts, max_followers)
mybot.login()
mybot.search_accounts(hashtags)
mybot.close_browser()