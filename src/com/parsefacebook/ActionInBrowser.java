package com.parsefacebook;

import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

public class ActionInBrowser {
    private WebDriver driver;
    private Properties config;
    static Logger logger = Logger.getLogger(ActionInBrowser.class.getName());

    private void setupBrowser() {
        logger.log(Level.INFO, "Start browser`s setup");
        Map<String, Object> prefs = new HashMap<String, Object>();
        prefs.put("profile.default_content_setting_values.notifications", 2);
        ChromeOptions options = new ChromeOptions();
        options.setExperimentalOption("prefs", prefs);
        driver = new ChromeDriver(options);
        logger.log(Level.INFO, "Open driver");
        driver.manage().window().maximize();
        logger.log(Level.INFO, "End browser`s setup");
    }

    public ActionInBrowser(Properties config) {
        logger.log(Level.INFO, "called constructor \"ActionInBrowser\"");
        this.config = config;
        setupBrowser();
    }

    public void changeSite(String url) {
        logger.log(Level.INFO, "trying get url");
        try{
            driver.get(url);
            logger.log(Level.INFO, "get new url successful");
        }
        catch (org.openqa.selenium.InvalidArgumentException ex) {
            logger.log(Level.WARNING, String.format("url is invalid, set google.com, exception: %s"), ex);
            driver.get("https://google.com/");
        }

        WebDriverWait wait = new WebDriverWait(driver, 10);
        logger.log(Level.INFO, "waiting load site");
        wait.until(ExpectedConditions.presenceOfAllElementsLocatedBy(new By.ByCssSelector("div")));

    }

    public void loginInFaceBook() {
        if (driver.getCurrentUrl() != "https://www.facebook.com/")
            driver.get("https://www.facebook.com/");

        logger.log(Level.INFO, "start login in facebook");

        String login = this.config.getProperty("LOGIN");
        String password = this.config.getProperty("PASSWORD");

        if (login == "phonenumber" || password == "password")
        {
            logger.log(Level.WARNING, "you need change login and password in config");
            throw new InvalidArgumentException("you need change login and password in config");
        }

        var config = ActionInBrowser.class.getResourceAsStream("config.properties");
        WebElement textBoxLogin = driver.findElement(new By.ById("email"));
        textBoxLogin.sendKeys(login);

        WebElement textBoxPass = driver.findElement(new By.ById("pass"));
        textBoxPass.sendKeys(password);

        WebElement buttonLogin = driver.findElement(new By.ByTagName("button"));
        buttonLogin.click();

        WebDriverWait wait = new WebDriverWait(driver, 10);
        logger.log(Level.INFO, "waiting load site before login");
        wait.until(ExpectedConditions.presenceOfAllElementsLocatedBy(new By.ByCssSelector("div")));
    }

    public void scrollInBottom() {
        logger.log(Level.INFO, "start scroll page with js");
        ((JavascriptExecutor) driver).executeScript(String.join("\n",
                "for(let i = 0; i < 50; i++)",
                "{",
                "   setTimeout(scroll, 500)",
                "}",
                "function scroll()",
                "{",
                "window.scrollBy(0, 1500);",
                "console.log(\"scroll\");",
                "}"));
    }

    public WebDriver getDriver() {
        return driver;
    }
}
