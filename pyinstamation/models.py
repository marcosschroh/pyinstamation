import peewee as orm
from playhouse.sqlite_ext import SqliteExtDatabase


db = SqliteExtDatabase('my_database.db')


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
    unfollow_date = orm.DateTimeField()
    following = orm.BooleanField()
    times_followed = orm.IntegerField(default=0)
