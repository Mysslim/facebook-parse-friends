package com.parsefacebook;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

public class JsonRepository implements Repository{
    static Logger logger = Logger.getLogger(TypeFriend.class.getName());
    private Properties config;

    public JsonRepository(Properties config) {
        this.config = config;
    }

    @Override
    public void insert(List<User> users) {
        JSONObject friends = new JSONObject();
        JSONArray list = new JSONArray();
        logger.log(Level.INFO, "start make json object");
        for (User friend : users) {
            JSONObject object = new JSONObject();
            object.put("fullname", friend.getFullname());
            object.put("addressToProfile", friend.getAddressToProfile());
            object.put("addressToAvatar", friend.getAddressToAvatar());
            list.add(object);
            logger.log(Level.INFO, String.format("add friend %s", friend.getFullname()));
        }
        friends.put("friends", list);
        logger.log(Level.INFO, "insert all friend in list");

        try {
            FileWriter writer = new FileWriter(config.getProperty("PATH_TO_JSON"));
            logger.log(Level.INFO, "create file writer");
            writer.write(friends.toJSONString());
            logger.log(Level.INFO, "write list with friend");
            writer.flush();
            logger.log(Level.INFO, "clear buffers, etc");
            writer.close();
            logger.log(Level.INFO, "close writer");
        } catch (IOException e) {
            logger.log(Level.OFF, "file is not found");
            return;
        }
    }

    @Override
    public boolean update(User oldUser, User newUser) {
        return false;
    }

    @Override
    public boolean delete(User user) {
        return false;
    }
}
