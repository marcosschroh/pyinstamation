import datetime
import logging
import peewee
from pyinstamation.models import User, Follower, future_rand_date, db


logger = logging.getLogger(__name__)


def create_tables(database):
    database.connect()
    database.create_tables([User, Follower], safe=True)


create_tables(db)


class Controller:

    def __init__(self, username):
        assert username is not None, 'username must be provided'

        user, is_new = User.get_or_create(username=username)
        self.user = user
        self.is_new = is_new

    def get_users_to_unfollow(self):
        return (self.user.follower_set.select(Follower.username, Follower.following)
                                      .where(Follower.following == True,  # noqa
                                             Follower.unfollow_date < datetime.datetime.now()))

    def get_users_following(self):
        return (self.user.follower_set.select(Follower.username, Follower.following)
                                      .where(Follower.following == True)) # noqa

    def set_users_followed(self, users):
        """
        :type users: list(namedtuple)
        """
        count = 0
        for user in users:
            unfollow_date = future_rand_date(date=user.follow_date)
            Follower.create(user=self.user, username=user.username, unfollow_date=unfollow_date)
            count += 1
        return count

    def set_users_unfollowed(self, users):
        """
        :type users: list(namedtuple)
        """
        usernames = [user.username for user in users]
        query = (Follower.update(following=False)
                         .where(Follower.username in usernames,
                                Follower.following == True,  # noqa
                                Follower.user == self.user.id))
        modified_rows = query.execute()
        return modified_rows

    def set_user_stats(self, likes=0, comments=0, followed=0, unfollowed=0, posts=0):
        self.user.likes += likes
        self.user.commented += comments
        self.user.followed += followed
        self.user.unfollowed += unfollowed
        self.user.save()
        logger.info('FINAL STATS')
        logger.info('Posts explored: %s', posts)
        logger.info('Likes: %s', likes)
        logger.info('Comments: %s', comments)
        logger.info('Followed: %s', followed)
        logger.info('Unfollowed: %s', unfollowed)

    def set_stats(self, bot):
        self.set_users_followed(bot.users_followed_by_bot)
        self.set_users_unfollowed(bot.users_unfollowed_by_bot)
        self.set_user_stats(likes=bot.likes_given_by_bot,
                            comments=bot.commented_post,
                            followed=len(bot.users_followed_by_bot),
                            unfollowed=len(bot.users_unfollowed_by_bot),
                            posts=bot.posts_explored)
        return True

    def run(self, bot):
        unfollow_users = self.get_users_to_unfollow()
        users_following = self.get_users_following()

        bot.run(users_to_unfollow=unfollow_users,
                users_following=users_following)

        self.set_stats(bot)
        db.close()
