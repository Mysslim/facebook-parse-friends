package com.parsefacebook;

import java.util.LinkedList;
import java.util.List;
import java.util.logging.Logger;

public class FriendBuilder {
    static Logger logger = Logger.getLogger(TypeFriend.class.getName());
    private ActionInBrowser browser;
    private TypeFriend activeFriend;

    public FriendBuilder(ActionInBrowser browser){
        this.browser = browser;
        this.activeFriend = new ActiveFriend(browser.getDriver());
    }

    public List<String> buildProfiles() {
        return activeFriend.getProfiles();
    }

    public List<String> buildFullname() {
        return activeFriend.getFullnames();
    }

    public List<String> buildAvatars() {
        return activeFriend.getAvatars();
    }
    public List<User> buildFriends() {
        List<String> profiles = buildProfiles();
        List<String> fullname = buildFullname();
        List<String> avatars = buildAvatars();

        List<User> friends = new LinkedList<>();
        for (int i = 0; i < avatars.size(); i++) {
            friends.add(new User(fullname.get(i), profiles.get(i), avatars.get(i)));
        }

        return friends;
    }

}
