import sys
from twitter import Twitter, OAuth, TwitterHTTPError
from twitter_follow_bot import auto_fav
import sqlite3 as lite
import string
import time

# put your tokens, keys, secrets, and twitter handle in the following variables
OAUTH_TOKEN = "291662316-"
OAUTH_SECRET = "zBK0"
CONSUMER_KEY = "ErQ"
CONSUMER_SECRET = "E0"
TWITTER_HANDLE = "username"
# name of the table in database for history
# sqlite> create table tweethistory(X integer primary key autoincrement,
# timestamp int, tweetid text, userid text);
HSTRYTAB = "tweethistory"

# filenames
BADWORDS = "badword.txt"
KEYWORDS = "keyword.txt"
BADUSERS = "baduser.txt"
HSTRYDBF = 'database.db'

NUMITEMS = 5

badword_list = [line.strip() for line in open(BADWORDS, 'r')]
keyword_list = [line.strip() for line in open(KEYWORDS, 'r')]
baduser_list = [line.strip() for line in open(BADUSERS, 'r')]

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET))

# favourite new tweets
for arg in keyword_list:
    print "Results for %s" % arg
    print "====================="
    userList = auto_fav(t, arg, count=NUMITEMS,
                        badwords=badword_list, badusers=baduser_list)

    cn = None
    try:
        cn = lite.connect(HSTRYDBF)
        for user in userList:
            cursor = cn.cursor()
            cursor.execute('INSERT INTO ' + HSTRYTAB +
                           '(timestamp, tweetid, userid)  VALUES (?, ?, ?);',
                           (time.time(), user[0], user[1]))
            cn.commit()
            print "Inserted user %s with id %s" % (user[0], user[1])
    except lite.Error, e:
        print "Error %s while storing favourite history" % e.args[0]

    finally:
        if cn:
            cn.close()

    print userList

#clean up old favs
following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

# don't unfav friends' tweets
whitelist = following | followers

cn = None
try:
    cn = lite.connect(HSTRYDBF)

    cursor = cn.cursor()

    upto = time.time() - 24*3600
    cursor.execute('select * from ' + HSTRYTAB +
                   ' where timestamp < ?;', (upto,))
    rows = cursor.fetchall()

    for row in rows:
        # if not
        if row[3] in whitelist:
            continue
        try:
            print "Unfavorited tweet by user %s" % row[3]
            t.favorites.destroy(_id=row[2], user_id=row[3])
        except TwitterHTTPError as e:
            print "Error %s while un-favouriting. ", e

    cursor.execute('delete from ' + HSTRYTAB +
                   ' where timestamp < ?;', (upto, ))
    cn.commit()

except lite.Error, e:
        print "Error %s while retrieving favourite history" % e.args[0]
finally:
    if cn:
        cn.close()
