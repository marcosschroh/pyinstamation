import datetime
import peewee as orm
from random import randrange
from playhouse.sqlite_ext import SqliteExtDatabase


db = SqliteExtDatabase('my_database.db')


def future_rand_date(date=None):
    if date is None:
        date = datetime.datetime.now()
    delta = {
        'days': randrange(2, 3),
        'hours': randrange(1, 4),
        'minutes': randrange(1, 60)
    }
    return date + datetime.timedelta(**delta)


class BaseModel(orm.Model):
    class Meta:
        database = db


class User(BaseModel):
    username = orm.CharField(unique=True)
    likes = orm.IntegerField(default=0)
    followed = orm.IntegerField(default=0)
    unfollowed = orm.IntegerField(default=0)
    commented = orm.IntegerField(default=0)


class Follower(BaseModel):
    user = orm.ForeignKeyField(User)
    username = orm.CharField()
    unfollow_date = orm.DateTimeField(default=future_rand_date)
    following = orm.BooleanField(default=True)
    times_followed = orm.IntegerField(default=1)
