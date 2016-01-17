from __future__ import unicode_literals

import re
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import signals
from django.utils import timezone
from celery.task.control import revoke

from battle.tasks import stream_twitter

def hashtag_validator(value):
    if not re.search('#[(\w+)]', value):
        raise ValidationError("Invalid format. Try #hashtag.")

def schedule_battle(sender, instance, **kwargs):
    if instance.task_id is not None:
        revoke(instance.task_id, terminate=True)

    eta = max(timezone.now(), instance.start_time)
    task = stream_twitter.apply_async([instance.id], eta=eta)
    Battle.objects.filter(id=instance.id).update(task_id=task.id)

class Hashtag(models.Model):
    value = models.CharField(max_length=140, validators=[hashtag_validator])

    def __str__(self):
        return "Hashtag: %s" % self.value

    def to_dict(self):
        data = dict(id=self.id, value=self.value)
        return data

class Battle(models.Model):
    name = models.CharField(max_length=32)
    hashtags = models.ManyToManyField(Hashtag, through='BattleHashtags')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    task_id = models.CharField(null=True, max_length=100)

    def __str__(self):
        return "%s (id: %d)" % (self.name, self.id)

    def get_winner(self):
        battle_hashtags = self.battlehashtags_set.all()
        return battle_hashtags.filter(words__gt=0).order_by('typos').first()

    def get_winner_by_ratio(self):
        winner_by_ratio = None
        winning_ratio = 1

        battle_hashtags = self.battlehashtags_set.all()
        for battle_hashtag in battle_hashtags:
            if battle_hashtag.words:
                ratio = float(battle_hashtag.typos) / battle_hashtag.words
                if ratio < winning_ratio:
                    winner_by_ratio = battle_hashtag
                    winning_ratio = ratio
        return winner_by_ratio

signals.post_save.connect(schedule_battle, sender=Battle)

class BattleHashtags(models.Model):
    hashtag = models.ForeignKey(Hashtag)
    battle = models.ForeignKey(Battle)
    typos = models.IntegerField(default=0)
    words = models.IntegerField(default=0)

    def to_dict(self):
        data = self.hashtag.to_dict()
        data['typos'] = self.typos
        data['words'] = self.words
        return data
