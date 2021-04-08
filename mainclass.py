import sys
import os
import logging
import configparser

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.firefox import GeckoDriverManager
from storages import CSVRepository, JSONRepository
from constants import *

class Main:
    def __init__(self):
        self.__setup_config()
        self.__setup_logger()
        self.__setup_driver()
        self.__count_of_friends = 0

    def get_config(self):
        return self.__config

    def get_count_friend(self):
        return self.__count_of_friends

    def __setup_logger(self):
        logging.basicConfig(
            filename = self.__config["Logger"]["FOLDER_FOR_LOG"] + "/" + self.__config["Logger"]["NAME_LOG_FILE"],
            filemode = self.__config["Logger"]["FILE_MODE_LOG"],
            level = self.__config["Logger"]["LEVEL_LOG"],
            format = "%(asctime)s-%(levelname)s-%(message)s")

    def __setup_config(self):
        self.__config = configparser.ConfigParser()
        try:
             self.__config.read("config.ini")

        except FileNotFoundError:
            print("config not found. Stop working")
            sys.exit()

        except Exception:
            print("an unexpected exception occurred")
            sys.exit()

    def __setup_driver(self):
        logging.debug("start setup driver")
        options = webdriver.FirefoxOptions()

        executable_path = GeckoDriverManager(path = self.get_path_to("./")).install()
        logging.debug("check new version driver and try install, return path to driver, path: {0}".format(executable_path))
        options.add_argument("--no-sandbox")
        options.add_argument("--single-process")
        options.add_argument("--disable-notifications")
        logging.debug("add arguments")

        self.__driver = webdriver.Firefox(executable_path=executable_path, options=options, log_path=self.__config["Logger"]["FOLDER_FOR_LOG"] + "/geckodriver.log")
        self.__driver.delete_all_cookies()
        self.__driver.maximize_window()
        logging.debug("end setup driver")

    def get_path_to(self, str: str) :
        return os.path.abspath(str)

    def set_count_friend(self, count : int):
        self.__count_of_friends = count

    def exit(self):
        self.__driver.close()
        sys.exit()

    
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

    def wait_for_item_load(self, by: By, path: str, element : str):
        try:
            logging.debug("waiting {0} form".format(element))
            self.wait_by_the_rule(expected_conditions.visibility_of_element_located((by, path)))

        except NoSuchElementException:
            logging.error("{0} not found exit".format(element))

        except TimeoutException:
            logging.error("timeout expired for {0}, exit".format(element))
            self.exit()

    def wait_until_item_is_clickable(self, by: By, path: str, element: str):
        try:
            logging.debug("waiting until {0} is clickable".format(element))
            self.wait_by_the_rule(expected_conditions.element_to_be_clickable((by, path)))

        except NoSuchElementException:
            logging.error("{0} not found exit".format(element))

        except TimeoutException:
            logging.error("timeout expired for {0}, exit".format(element))
            self.exit()

    def login_in_facebook(self):
        self.check_argv()
        script_name, login, passwd = sys.argv

        self.wait_until_item_is_clickable(By.ID, SELECTOR_FOR_LOGIN, "text_box_login")

        self.__driver.find_element(By.ID, SELECTOR_FOR_LOGIN).send_keys(login)
        self.__driver.find_element(By.ID, SELECTOR_FOR_PASSWD).send_keys(passwd)
        self.__driver.find_element(By.TAG_NAME, SELECTOR_FOR_BUTTON).click()

    def get_path_to_friend_in_panel(self, index : int):
        if index <= 0:
            logging.warning("friend index not be less 0")
            index = 1
        return "{0}[{1}]".format(PATH_TO_FRIEND, index) 

    def move_to_myprofile(self):
        self.wait_for_item_load(By.CSS_SELECTOR, PATH_TO_MYPROFILE, "button_my_profile")
        self.__driver.find_element(By.CSS_SELECTOR, PATH_TO_MYPROFILE).click()

    def move_to_friends(self):
        self.wait_for_item_load(By.XPATH, PATH_TO_DROP_DOWN_FORM, "drop_down_form")
        drop_down_form = self.__driver.find_element(By.XPATH, PATH_TO_DROP_DOWN_FORM)
        drop_down_form.click()

        self.wait_for_item_load(By.XPATH, PATH_TO_COUNT_FRIENDS, "count_friend")
        self.set_count_friend(int(self.__driver.find_element(By.XPATH, PATH_TO_COUNT_FRIENDS).text))

        self.wait_for_item_load(By.XPATH, PATH_TO_BUTTON_FRIENS, "button_friends")
        self.__driver.find_elements(By.XPATH, PATH_TO_BUTTON_FRIENS)[0].click()

    def get_DOM_friends(self):
        web_element_friends = []
        
        while len(web_element_friends) < self.get_count_friend():
            self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

            self.wait_for_item_load(By.CSS_SELECTOR, PATH_TO_FRIEND, "friends")
            web_element_friends = self.__driver.find_elements(By.CSS_SELECTOR, PATH_TO_FRIEND)

        return web_element_friends 

    def get_info_about_friends(self):
        web_element_friends = self.get_DOM_friends()
        friends = []

        for friend in web_element_friends:
            info_friend = []
            info_friend.append(friend.find_element(By.CSS_SELECTOR, PATH_ADDRESS_IN_PROFILE).get_attribute("href"))
            info_friend.append(friend.find_element(By.CSS_SELECTOR, PATH_FULLNAME).text)
            
            friends.append(info_friend)

        return friends

    def workflow(self):
        
        self.__driver.get("https://www.facebook.com/")
        self.login_in_facebook()
        self.move_to_myprofile()
        self.move_to_friends()
        friends = self.get_info_about_friends()

        repository = CSVRepository(self.get_config())
        repository.insert(friends)

        repository = JSONRepository(self.get_config())
        repository.insert(friends)

        self.__driver.close()

    