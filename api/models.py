from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hour = models.IntegerField()
    note = models.CharField('what to do', max_length=1024)

    def to_json(self):
        return {'user_id': self.user.id, 'task_id': self.id, 'date': self.date, 'hour': self.hour, 'note': self.note}

    def __unicode__(self):
        return self.note


class Setting(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            primary_key=True,
    )
    preferred_hour = models.IntegerField(default=0)

    def is_under(self, date):
        return self.preferred_hour > sum([task.hour for task in self.user.task_set.filter(date=date)])

    def to_json(self):
        return {'user_id': self.user.id, 'username': self.user.username, 'task_count': len(self.user.task_set.all()),
                'preferred_hour': self.preferred_hour}

    def __unicode__(self):
        return str(self.preferred_hour)
