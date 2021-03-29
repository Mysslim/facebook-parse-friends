package com.parsefacebook;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

public abstract class TypeFriend {
    static Logger logger = Logger.getLogger(TypeFriend.class.getName());
    protected WebDriver driver;
    protected WebElement panelFriend;

    public abstract List<String> getAvatars();
    public abstract List<String> getFullnames();
    public abstract List<String> getProfiles();
    public List<WebElement> getWebElements(By locator) {
        List<WebElement> elements;
        setPanelFriend();

        WebDriverWait wait = new WebDriverWait(driver, 3);
        try {
            logger.log(Level.INFO, "waiting load all friends");
            wait.until(ExpectedConditions.numberOfElementsToBe(locator, getCoutFriend()));
        }
        catch (org.openqa.selenium.TimeoutException ex) {
            logger.log(Level.WARNING, "load not all friends");
            wait.until(ExpectedConditions.numberOfElementsToBeLessThan(locator, getCoutFriend()));
        } catch (org.openqa.selenium.InvalidSelectorException ex) {
            logger.log(Level.OFF, String.format("Incorrect selector, return null. exception: %s", ex));
            return null;

        } catch (org.openqa.selenium.StaleElementReferenceException ex) {
            logger.log(Level.OFF, String.format("panelFriend is out of date, update panelFriend. exception: %s", ex));
            setPanelFriend();
        }
        elements = panelFriend.findElements(locator);
        logger.log(Level.INFO, "getting friends");
        return elements;
    }

    public void setPanelFriend() {
        WebDriverWait wait = new WebDriverWait(driver, 5);
        wait.until(ExpectedConditions.visibilityOfElementLocated(new By.ByXPath(Constants.xpathToPanelFriends)));

        panelFriend = driver.findElement(new By.ByXPath(Constants.xpathToPanelFriends));
    }

    public int getCoutFriend() {
        return 50;
    }
}
