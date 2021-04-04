

import sys
import os
import logging
import configparser

from selenium import webdriver
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.firefox import GeckoDriverManager
from storages import CSVRepository, JSONRepository
from constants import *

class Main:
    def __init__(self):
        self.__config = self.__setup_config()
        self.__driver = self.__setup_driver()

    def get_config(self):
        return self.__config

    def get_count_friend(self):
        return COUNT_OF_FRIEND

    def setup_logger(self):
        logging.basicConfig(
            filename = self.__config["Logger"]["FOLDER_FOR_LOG"] + "/" + self.__config["Logger"]["NAME_LOG_FILE"],
            filemode = self.__config["Logger"]["FILE_MODE_LOG"],
            level = self.__config["Logger"]["LEVEL_LOG"],
            format = "%(asctime)s-%(levelname)s-%(message)s")

    def __setup_config(self):
        config = configparser.ConfigParser()
        try:
            config.read("config.ini")

        except FileNotFoundError:
            print("config not found. Stop working")
            sys.exit()

        except Exception:
            print("an unexpected exception occurred")
            sys.exit()

        return config

    def get_path_to(self, str: str) :
        return os.path.abspath(str)

    def __setup_driver(self):
        logging.debug("start setup driver")
        options = webdriver.FirefoxOptions()

        executable_path = GeckoDriverManager(path = self.get_path_to("./")).install()
        logging.debug("check new version driver and try install, return path to driver, path: {0}".format(executable_path))

        options.add_argument("--start-maximized")   # fullscreen
        options.add_argument("--no-sandbox")
        options.add_argument("--single-process")
        options.add_argument("--disable-notifications")
        logging.debug("add arguments")

        driver = webdriver.Firefox(executable_path=executable_path, options=options, log_path=self.__config["Logger"]["FOLDER_FOR_LOG"] + "/geckodriver.log")
        driver.delete_all_cookies()
        logging.debug("end setup driver")

        return driver

    def check_argv(self):
        try:
            script, login, passwd = sys.argv
        except ValueError:
            logging.error("you need input login and password, call exception")
            raise ValueError("you need input login and password") 
        
        logging.debug("argv is correct")

    def wait_by_the_rule(self, rule):
        wait = WebDriverWait(self.__driver, int(self.__config["Timer"]["SECOND"]))
        wait.until(rule)

    def login_in_facebook(self):
        self.check_argv()
        script, login, passwd = sys.argv

        if self.__driver.current_url != "https://www.facebook.com/":
            logging.warning("url is not facebook, change url")
            self.__driver.get("https://www.facebook.com/")

        self.wait_by_the_rule(expected_conditions.element_to_be_clickable((By.ID, "email")))

        text_box_login = self.__driver.find_element(By.ID, SELECTOR_FOR_LOGIN)
        text_box_login.send_keys(login)

        text_box_login = self.__driver.find_element(By.ID, SELECTOR_FOR_PASSWD)
        text_box_login.send_keys(passwd)

        button_login = self.__driver.find_element(By.TAG_NAME, SELECTOR_FOR_BUTTON)
        button_login.click()

    def scrollInBottom(self):
        self.wait_by_the_rule(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "div")))

        javascript = """
        for(let i = 0; i < 50; i++) {
            scroll()
            setTimeout(scroll, 2000)
            
        }
        function scroll() { 
            window.scrollBy(0, 3000);
        }
        """

        logging.debug("make script")
        self.__driver.execute_script(javascript)
        logging.debug("execute script")

    def get_locator_path(self, panel, path_to):
        css_path = "{0}[class='{1}'] {2}".format(
            panel.tag_name, 
            panel.get_attribute("class"),
            path_to)

        return css_path

    def get_panel_friend(self):
        panel = None

        self.wait_by_the_rule(expected_conditions.visibility_of_element_located((By.XPATH, XPATH_TO_PANEL_FRIENDS_FIREFOX)))
        panel = self.__driver.find_element(By.XPATH, XPATH_TO_PANEL_FRIENDS_FIREFOX)
        
        return panel

    def get_web_elements(self, by: By, path: str, panel):
        web_elements = None

        try:
            logging.debug("waiting load all friends")
            self.wait_by_the_rule(expected_conditions.number_of_windows_to_be(((by, path), self.get_count_friend())))

        except TimeoutException:
            logging.error("not all friends are loaded")

        except InvalidSelectorException:
            logging.error("incorrect selector, return None")
            return None
        try:
            web_elements = panel.find_elements(by, path)
        
        except StaleElementReferenceException:
            logging.error("panelFriend is out of date, update panelFriend.")
            panel = self.get_panel_friend()
            web_elements = panel.find_elements(by, path)
         
        return web_elements

    def get_friends(self):
        friends = []
        fullnames = self.get_fullname_friends()
        profiles = self.get_profiles_friends()
        avatars = self.get_avatars_friends()

        count = len(fullnames)

        for friend in range(count):
            friends.append([fullnames[friend], profiles[friend], avatars[friend]])
        
        return friends

    def get_fullname_friends(self):
        logging.debug("start getting fullname friends")
        panel = self.get_panel_friend()
        
        elements = self.get_web_elements(By.CSS_SELECTOR, self.get_locator_path(panel, PATH_FULLNAME_ACTIVE), panel)

        fullnames = []
        for element in elements:
            fullnames.append(element.text)

        logging.debug("return")
        return fullnames
    
    def get_profiles_friends(self):
        logging.debug("start getting profile friends")
        panel = self.get_panel_friend()
        
        elements = self.get_web_elements(By.CSS_SELECTOR, self.get_locator_path(panel, PATH_ADDRESS_IN_PROFILE), panel)
        profiles = []
        for element in elements:
            profiles.append(element.get_attribute("href"))

        logging.debug("return")
        return profiles

    def get_avatars_friends(self):
        logging.debug("start getting avatar friends")
        panel = self.get_panel_friend()
        
        elements = self.get_web_elements(By.CSS_SELECTOR, self.get_locator_path(panel, PATH_IMG_ACTIVE), panel)
        avatars = []
        for element in elements:
            avatars.append(element.get_attribute("src"))

        logging.debug("return")
        return avatars

    def workflow(self):
        
        self.__driver.get("https://www.facebook.com/")
        self.login_in_facebook()
        self.__driver.get("https://www.facebook.com/profile.php?id=100017172458807&sk=friends&ft_ref=flsa")
        self.scrollInBottom()
        friends = self.get_friends()
        
        repository = CSVRepository(self.get_config())
        repository.insert(friends)

        repository = JSONRepository(self.get_config())
        repository.insert(friends)

        self.__driver.close()

    