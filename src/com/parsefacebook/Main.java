package com.parsefacebook;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.List;
import java.util.Properties;
import java.util.logging.LogManager;

public class Main {
    private ActionInBrowser browser;
    private FriendBuilder builder;
    private Repository repository;

    public Properties setupConfig() {
        FileInputStream file;
        Properties config = new Properties();
        try {
            file = new FileInputStream("src/resources/config.properties");
            config.load(file);
        }
        catch (IOException ex)
        {
            System.err.print("File is not exists");
            return null;
        }
        return config;
    }

    public void setupLogger () {
        try {
            LogManager.getLogManager().readConfiguration(
                    Main.class.getResourceAsStream("/logging.properties"));
        }
        catch (IOException e) {
            System.err.println("Couldnot setup logger configuration: " + e.toString());
        }
    }

    public void setup() {
        //setupLogger();
        Properties config = setupConfig();
        browser = new ActionInBrowser(config);
        builder = new FriendBuilder(browser);
        repository = new JsonRepository(config);
    }

    public void workFlow() {
        browser.changeSite("https://www.facebook.com/");
        browser.loginInFaceBook();
        browser.changeSite("https://www.facebook.com/profile.php?id=100017172458807&sk=friends&ft_ref=flsa");
        browser.scrollInBottom();

        FriendBuilder builder = new FriendBuilder(browser);
        List<User> friends = builder.buildFriends();
        repository.insert(friends);

    }


    public static void main(String[] args) {
        Main main = new Main();
        main.setup();
        main.workFlow();
    }
}
