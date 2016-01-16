from __future__ import unicode_literals

import json

from django.utils import timezone
from threading import Timer
from django.conf import settings
from djcelery import celery

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from enchant.checker import SpellChecker

class TwitterStreamListener(StreamListener):
    def __init__(self, battle_hashtags):
        super(TwitterStreamListener, self).__init__()
        self.battle_hashtags = battle_hashtags

    def on_data(self, text):
        data = json.loads(text)
        print data
        for battle_hashtag in self.battle_hashtags:
            print 'value', battle_hashtag.hashtag.value.lower()
            print 'tweet', data['text'].lower()
            print battle_hashtag.hashtag.value.lower() in data['text'].lower()
            if battle_hashtag.hashtag.value.lower() in data['text'].lower():
                checker = SpellChecker('en_GB')
                checker.set_text(data['text'])
                for typo in checker:
                    print 'typo', typo.word
                    battle_hashtag.typos+=1

                battle_hashtag.save()

        return True

    def on_error(self, status):
        if status == 420:
            print 'Twitter has rate limitted this application. Please try again a little bit later.'
        else:
            print 'Twitter error code', status

@celery.task
def stream_twitter(battle_id):
    #Avoiding circular import
    from battle.models import Battle

    battle = Battle.objects.get(id=battle_id)
    if battle.end_time < timezone.now():
        return

    battle.battlehashtags_set.update(typos=0)
    battle_hashtags = battle.battlehashtags_set.all().prefetch_related('hashtag')

    hashtag_values = [x.hashtag.value for x in battle_hashtags]

    listener = TwitterStreamListener(battle_hashtags)
    auth = OAuthHandler(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET
    )

    auth.set_access_token(
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET
    )

    stream = Stream(auth, listener)

    delay = battle.end_time - timezone.now()
    print 'delay', delay, delay.total_seconds(), hashtag_values
    Timer(delay.total_seconds(), stream.disconnect).start()

    stream.filter(track=hashtag_values, languages = ['en'])
