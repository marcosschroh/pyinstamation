# PYINSTAMATION

> Easy to use, config oriented, instagram bot, written in python 3

[![Build Status](https://travis-ci.org/discov-r/pyinstamation.svg?branch=master)](https://travis-ci.org/discov-r/pyinstamation)
[![codecov](https://codecov.io/gh/discov-r/pyinstamation/branch/master/graph/badge.svg)](https://codecov.io/gh/discov-r/pyinstamation)


![](./docs/demo.gif)

## Features

- [x] Upload pictures
- [x] Farm followers with the follow/unfollow technique
- [x] Like and comment by tags
- [x] Metrics persisted in db
- [x] Logging
- [x] Comment generator
- [ ] Daemonize and upload pics/vids at exact time
- [ ] Support for plugins
- [ ] Web with graphs and statistics
- [ ] Dockerization
- [ ] Auto update user's description

## TODO

These will be removed once completed

- [ ] Gather more posts to like (currently it does not reach the max likes to give )
- [ ] Finish tests
- [ ] Track number of followers and following per day


Note: The internal API of `bot.py` may change.


## Supported OS

```
Linux (Tested in debian)
OS X
```


## Requirements

```
python 3
```

Remember to create a [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)


## Installation

`pip install -r requirements.txt`


## Usage

| Command | Description |
| --- | --- |
| `make init` | Downloads webdriver and creates a new conf based on the default one |
| `make run-bot` | Starts running the bot (remember to at least set the username and password) |


## Configuration

Create a `config.yaml` and tune it at will, or use `make init`.
The options are divided in different sections.

| Option | Type | Description |
| --- | --- | --- |
| `username` * | str | instagram username to operate with |
| `password` ** | str | username's password |
| `hide_browser` | bool | does not display the browser |

\*  Required

** Required unless the bot is launched with `-p [PASSWORD]`


### Posts

| Option | Type | Description | Default |
| --- | --- | --- | --- |
| `search_tags` | str | comma separated tags to search for | [] |
| `ignore_tags` | str | comma separated tags to ignore if a post contains them while searching | [] |
| `posts_per_hashtag` | int | number of posts to be processed per hashtag |
| `likes_per_day` | int | maximum likes given in a day | 100 |
| `like_probability` | float | probability to give a like | 0.5 |
| `comments_per_day` | int | maximum comments given in a day | 10 |
| `comment_probability` | float| probability to comment | 0.5 |
| `comment_enabled` | bool| bot will comment in the searched posts | True |
| `comment_generator` | bool | bot will generate a random generic comment | True |
| `custom_comments` | array | in case you don't want random comments, you can provide them | [] |
| `total_to_follow_per_hashtag` | int | number of users to follow per each hashtag | 10 |

### Followers

| Option | Type | Description | Default |
| --- | --- | --- | --- |
| `follow_enable` | bool | while searching the bot will also follow people | True |
| `min_followers` | int | minimum number followers that a user must have to follow. Lower bound | 0 |
| `max_followers` | int | will follow users with less than this amount of followers. Upper bound | 0 |
| `follow_probability` | float | chance to follow someone while searching, between 0 and 1 | 0.5 |
| `ignore_users` | array | users not to follow | [] |
| `follow_per_day` | int | max number of users to follow | 50 |
| `unfollow_followed_users` | bool | after a few days the bot will stop following the users followed | True |

### Pics

| Option | Type | Description | Default |
| --- | --- | --- | --- |
| `upload` | bool | when enabled attempts to upload a picture if there is one to upload | False |
| `files` | collection | the contents of the files to upload are below | [] |

#### Pics > files

| Option | Type | Description | Default |
| --- | --- | --- | --- |
| `path` * | str | absolute path to the file location. |
| `datetime` | str | format ISO 8061: `%Y-%m-%dT%H:%M:%S` eg: `2017-08-18T18:00:00`. For now, time is ignored, but the idea is to take it into account | None |
| `comment` | str | comment to be added when the pic is posted  | None |

\*  Required

For config template check [default.config.yaml](./default.config.yaml)


We told you it was easy.
