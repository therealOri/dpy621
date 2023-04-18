# dpy621
Python3 discord bot code for interacting with the e621 api for all my furry fellows uwu.


I was looking around for a long time and couldn't find any simple documentation to easily work with the e621 api. So I decided to make my own e621 command and allow you guys to use it in your bots too! provided you give creddit and not just rip the code and say you made it. This took me about 2 days to make.

<br />
<br />

# Links
[Api Documentation](https://e621.net/help/api)

[Make an account](https://e621.net/users/new)

[DB Browser](https://sqlitebrowser.org/dl/)
> __ __
> After making an account, click on "Account" in the top left. Then click on "Manage Api Access". Enter your password and copy said api key. If you already have an account or don't want to make one for your bot to use then you can just login instead of makning an account and follow the same steps mentioned.
> __ __
#

<br />
<br />

# Installation
```bash
[therealOri ~]$ git clone https://github.com/therealOri/dpy621.git
[therealOri ~]$ cd dpy621
[therealOri ~]$ pip install -r requirements.txt
```
> You can run the following command if a module/package isn't found.
> - [therealOri ~]$ pip install <module name that isn't found>

<br />
<br />
<br />


# Disclaimer
Due to the way e621 tags their posts you may still get some unwanted content slipping through. This is in part because of a bad post having the tag "gay"(for example) along side of the tag you have blacklisted. This code prevents users from including said tag in their agument/search request and that's about it. There isn't anything I can do about this as it happens even in the website with blacklisted tags enabled and still seeing said content. (If you use e621 a lot then you know what I am talking about in this disclaimer).
