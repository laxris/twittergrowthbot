#Twitter Follow Bot

A Python bot that can automatically follow users and favorite tweets associated with a specific search query on Twitter. Also has the ability to unfollow all users not currently following you back.

##Disclaimer

I hold no liability for what you do with this script or what happens to you by using this script. Abusing this script *can* get you banned from Twitter, so make sure to read up on proper usage of the Twitter API.

##Setup

Setup a file of keywords to favorite, a list of bad words to exclude (so no offensive tweets get favorited) and set your own name on the list of users to abvoid. Make sure your the database file is initialized, e.g. by using the sqlite3 tool:

sqlite3 filename.db
create table tweethistory(X integer primary key autoincrement, timestamp int, tweetid text, userid text);
.exit

Enter your oauth-date into the corresponding fields. If you don't have app access yet, follow these instructions to create your own app:

Go to https://dev.twitter.com/apps

1. Sign in with your Twitter account
2. Create a new app account
3. Modify the settings for that app account to allow read & write
4. Generate a new OAuth token with those permissions
5. Manually edit the script and put those tokens in the script


##Dependencies

You will need to install Python's `twitter` library first:

    easy_install twitter
    

##Licence

Published under GPL 3 by Chris Hammerschmidt (http://chrishammerschmidt.de), based functions of the twitter-follow-bot library  https://github.com/rhiever/twitter-follow-bot by Randal S. Olson (http://www.randalolson.com)