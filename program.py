import sys
import os
import logging
import configparser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.firefox import GeckoDriverManager

def setup_logger(config):
    logging.basicConfig(
        filename = config["Logger"]["FOLDER_FOR_LOG"] + "/" + config["Logger"]["NAME_LOG_FILE"],
        filemode = config["Logger"]["FILE_MODE_LOG"],
        level = config["Logger"]["LEVEL_LOG"],
        format = "%(asctime)s-%(levelname)s-%(message)s")

def setup_config():
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

def get_path_to(str) :
    return os.path.abspath(str)

def setup_driver_and_return(config):
    logging.debug("start setup driver")
    options = webdriver.FirefoxOptions()

    executable_path = GeckoDriverManager(path=get_path_to("./")).install()
    logging.debug("check new version driver and try install, return path to driver, path: {0}".format(executable_path))

    options.add_argument("--start-maximized")   # fullscreen
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")
    options.add_argument("--disable-notifications")
    logging.debug("add arguments")

    driver = webdriver.Firefox(executable_path=executable_path, options=options, log_path=config["Logger"]["FOLDER_FOR_LOG"] + "/geckodriver.log")
    driver.delete_all_cookies()
    logging.debug("end setup driver")

    return driver

def check_argv():
    try:
        script, login, passwd = sys.argv
    except ValueError:
        logging.error("you need input login and password, call exception")
        raise ValueError("you need input login and password") 
    
    logging.debug("argv is correct")

def wait_by_the_rule(driver: webdriver, seconds: int, rule):
    wait = WebDriverWait(driver, seconds)
    wait.until(rule)

def login_in_facebook(config, driver: webdriver):
    check_argv()
    script, login, passwd = sys.argv

    if driver.current_url != "https://www.facebook.com/":
        logging.warning("url is not facebook, change url")
        driver.get("https://www.facebook.com/")

    wait_by_the_rule(
        driver, 
        int(config["Timer"]["SECOND"]), 
        expected_conditions.element_to_be_clickable((By.ID, "email")))

    text_box_login = driver.find_element(By.ID, "email")
    text_box_login.send_keys(login)

    text_box_login = driver.find_element(By.ID, "pass")
    text_box_login.send_keys(passwd)

    button_login = driver.find_element(By.TAG_NAME, "button")
    button_login.click()

def scrollInBottom(config, driver: webdriver):
    wait_by_the_rule(
        driver,
        int(config["Timer"]["SECOND"]),
        expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "div")))

    javascript = """
    for(let i = 0; i < 25; i++) {
        scroll()
        setTimeout(scroll, 2000)
        
    }
    function scroll() { 
        window.scrollBy(0, 2000);
    }
    """

    logging.debug("make script")
    driver.execute_script(javascript)
    logging.debug("execute script")

def get_friends():
    return None

def workflow(config, driver):
    driver.get("https://www.facebook.com/")
    login_in_facebook(config, driver)
    driver.get("https://www.facebook.com/profile.php?id=100017172458807&sk=friends&ft_ref=flsa")
    scrollInBottom(config, driver)
    friends = get_friends(config, driver)

if __name__ == "__main__":
    config = setup_config()
    setup_logger(config)
    driver = setup_driver_and_return(config)
    workflow(config, driver)