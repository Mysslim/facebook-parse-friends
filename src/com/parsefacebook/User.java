package com.parsefacebook;

public class User {
    private String fullname;
    private String addressToProfile;
    private String addressToAvatar;

    public User(String fullname, String addressToProfile, String addressToAvatar) {
        this.fullname = fullname;
        this.addressToProfile = addressToProfile;
        this.addressToAvatar = addressToAvatar;
    }

    public String getFullname() {
        return fullname;
    }

    public String getAddressToProfile() {
        return addressToProfile;
    }

    public String getAddressToAvatar() {
        return addressToAvatar;
    }

    public void setFullname(String fullname) {
        this.fullname = fullname;
    }

    public void setAddressToProfile(String addressToProfile) {
        this.addressToProfile = addressToProfile;
    }

    public void setAddressToAvatar(String addressToAvatar) {
        this.addressToAvatar = addressToAvatar;
    }
}
