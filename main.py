from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
import time
import random
import requests
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

    # method downloads content from user page
    def download_userpage_content(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        # create a folder with a username to keep the project clean
        if os.path.exists(f"{file_name}"):
            print("ERROR: The folder already exists!")
        else:
            os.mkdir(file_name)

        img_and_video_src_urls = []
        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list:
                try:
                    browser.get(post_url)
                    time.sleep(4)

                    img_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img"
                    video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
                    post_id = post_url.split("/")[-2]

                    if self.xpath_exists(img_src):
                        img_src_url = browser.find_element_by_xpath(img_src).get_attribute("src")
                        img_and_video_src_urls.append(img_src_url)

                        # save the image
                        get_img = requests.get(img_src_url)
                        with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)

                    elif self.xpath_exists(video_src):
                        video_src_url = browser.find_element_by_xpath(video_src).get_attribute("src")
                        img_and_video_src_urls.append(video_src_url)

                        # save the video
                        get_video = requests.get(video_src_url, stream=True)
                        with open(f"{file_name}/{file_name}_{post_id}_video.mp4", "wb") as video_file:
                            for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    video_file.write(chunk)
                    else:
                        img_and_video_src_urls.append(f"{post_url}, link not found!")
                    print(f"SUCCESS: content from post {post_url} downloaded!")

                except Exception as ex:
                    print(ex)
                    self.close_browser()

            self.close_browser()

        with open(f'{file_name}/{file_name}_img_and_video_src_urls.txt', 'a') as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")

    # subscription method for all subscribers of the transferred account
    def get_all_followers(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split("/")[-2]

        # create a folder with a username to keep the project clean
        if os.path.exists(f"{file_name}"):
            print(f"Folder {file_name} already exists!")
        else:
            print(f"Create user folder {file_name}.")
            os.mkdir(file_name)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f"User {file_name} does not exist, check URL")
            self.close_browser()
        else:
            print(f"User {file_name} was found successfully, let's start downloading subscriber links!")
            time.sleep(2)

            followers_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
            followers_count = followers_button.text
            followers_count = int(followers_count.split(' ')[0])
            print(f"Number of subscribers: {followers_count}")
            time.sleep(2)

            loops_count = int(followers_count / 12)
            print(f"Number of iterations: {loops_count}")
            time.sleep(4)

            followers_button.click()
            time.sleep(4)

            followers_ul = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

            try:
                followers_urls = []
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Iteration #{i}")

                all_urls_div = followers_ul.find_elements_by_tag_name("li")

                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                # save all user subscribers to a file
                with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

                with open(f"{file_name}/{file_name}.txt") as text_file:
                    users_urls = text_file.readlines()

                    for user in users_urls[0:10]:
                        try:
                            try:
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        print(f'We are already subscribed to {user}, move on to the next user!')
                                        continue

                            except Exception as ex:
                                print('The file with links has not been created yet!')
                                # print(ex)

                            browser = self.browser
                            browser.get(user)
                            page_owner = user.split("/")[-2]

                            if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div/a"):

                                print("This is our profile, already subscribed, skip iteration!")
                            elif self.xpath_exists(
                                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button/div/span"):
                                print(f"Already follow {page_owner} skip iteration!")
                            else:
                                time.sleep(random.randrange(4, 8))

                                if self.xpath_exists(
                                        "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                    try:
                                        follow_button = browser.find_element_by_xpath(
                                            "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                        print(f'We requested a subscription to user {page_owner}. Closed account!')
                                    except Exception as ex:
                                        print(ex)
                                else:
                                    try:
                                        if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button"):
                                            follow_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                            print(f'Subscribed to user {page_owner}. Open account!')
                                        else:
                                            follow_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button").click()
                                            print(f'Subscribed to user {page_owner}. Open account!')
                                    except Exception as ex:
                                        print(ex)

                                # we write data to a file for links of all subscriptions, if there is no file, we create it, if there is, we add
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)

                                time.sleep(random.randrange(7, 15))

                        except Exception as ex:
                            print(ex)
                            self.close_browser()

            except Exception as ex:
                print(ex)
                self.close_browser()

        self.close_browser()


mybot = InstagramBot(username, password)
mybot.login()
mybot.put_many_likes('https://www.instagram.com/lenabrand.official/')


















