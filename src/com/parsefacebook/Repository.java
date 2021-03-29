package com.parsefacebook;

import java.util.List;

public interface Repository {
    void insert(List<User> users);
    boolean update(User oldUser, User newUser);
    boolean delete(User user);
}
