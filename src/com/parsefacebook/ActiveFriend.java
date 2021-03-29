package com.parsefacebook;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.LinkedList;
import java.util.logging.Logger;
import java.util.List;

public class ActiveFriend extends TypeFriend{
    static Logger logger = Logger.getLogger(TypeFriend.class.getName());

    public ActiveFriend(WebDriver driver) {
        super.driver = driver;
    }

    @Override
    public List<String> getAvatars() {
        setPanelFriend();
        String strLocator = String.format("%s[class='%s'] %s", panelFriend.getTagName(), panelFriend.getAttribute("class"), Constants.pathImgActive);

        List<WebElement> elements = getWebElements(new By.ByCssSelector(strLocator));
        List<String> avatars = new LinkedList<String>();

        for (WebElement element : elements) {
            avatars.add(element.getAttribute("src"));
        }
        return avatars;
    }

        @Override
    public List<String> getFullnames() {
        setPanelFriend();
        String strLocator = String.format("%s[class='%s'] %s", panelFriend.getTagName(), panelFriend.getAttribute("class"), Constants.pathFullnameActive);

        List<WebElement> elements = getWebElements(new By.ByCssSelector(strLocator));
        List<String> fullnames = new LinkedList<String>();

        for (WebElement element : elements) {
            fullnames.add(element.getText());
        }

        return fullnames;
    }

    @Override
    public List<String> getProfiles() {
        setPanelFriend();
        String strLocator = String.format("%s[class='%s'] %s", panelFriend.getTagName(), panelFriend.getAttribute("class"), Constants.pathAddressInProfile);

        List<WebElement> elements = getWebElements(new By.ByCssSelector(strLocator));
        List<String> profiles = new LinkedList<String>();

        for (WebElement element : elements) {
            profiles.add(element.getAttribute("href"));
        }
        return profiles;
    }
}
