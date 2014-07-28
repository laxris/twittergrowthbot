"""
Copyright 2014 Chris Hammerschmidt

Based on the Twitter Follow Bot library as stated below.

Copyright 2014 Randal S. Olson

This file is part of the Twitter Follow Bot library.

The Twitter Follow Bot library is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

The Twitter Follow Bot library is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along with
the Twitter Follow Bot library. If not, see http://www.gnu.org/licenses/.
"""

import string
import time
from twitter import Twitter, OAuth, TwitterHTTPError


def search_tweets(t, q, count=100, result_type="recent"):
    """
        Returns a list of tweets matching a certain phrase
    """

    return t.search.tweets(q=q, result_type=result_type, count=count)


def auto_fav(t, q, badwords, badusers, result_type="recent", count=100):
    """
        Favorites tweets that match a certain phrase (hashtag, word, etc.)
    """

    result = search_tweets(t, q, count, result_type)
    alreadySeen = False
    userList = []

    for tweet in result['statuses']:
        try:
            # don't deal with specific users
            breaker = False
            for baduser in badusers:
                if string.find(tweet['user']['screen_name'].lower(),
                               baduser.lower()) != -1:
                    breaker = True
            if breaker:
                continue

            # don't deal with specific words from list
            breaker = False
            for badword in badwords:
                if string.find(tweet['text'].lower(), badword.lower()) != -1:
                    print "BADWORD: %s" % (tweet['text']).encode('utf-8')
                    breaker = True
            if breaker:
                continue

            # don't fav replies in conversations, people think it's creepy
            if tweet['in_reply_to_status_id']:
                continue

            # sometimes twitter API returns results with unset favorited value
            #favcheck = t.statuses.show(_id=tweet['id'])
            #if favcheck['favorited']:
            #    continue

            if tweet['favorited']:
                continue

            # actual fav
            result = t.favorites.create(_id=tweet['id'])
            result = tweet
            print "favorited: %s by %s" % ((result['text']).encode('utf-8'),
                                           result['user']['screen_name'].
                                           encode('utf-8'))
            userList.append((tweet['id'], result['user']['screen_name']))

        # when you have already favorited a tweet this error is thrown
        except TwitterHTTPError as e:
            # if you don't call statuses.show() for every tweet
            # the fav bit might be set wrongly by twitter
            if "status 403" in str(e).lower():
                print "already favorited"
                if alreadySeen:
                    break
                alreadySeen = True
            # better don't violate the api rate limit
            elif "status 429" in str(e).lower():
                print "RATE LMITED"
                quit()
            else:
                print "error: ", e

        # cheap rate limiting for max favs / day
        time.sleep(30)

    return userList
