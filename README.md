# PYINSTAMATION

> Easy to use instagram bot written in python 3


## Features

- [x] Upload pictures
- [x] Farm followers with the follow/unfollow technique
- [x] Like and comment by tags
- [x] Metrics persisted in db
- [x] Logging
- [ ] Comment generator
- [ ] Daemonize and upload pics/vids at exact time
- [ ] Support for plugins
- [ ] Web with graphs and statistics
- [ ] Dockerization


## TODO

These will be removed once completed

- [ ] Gather more posts to like (currently it does not reach the max likes to give )
- [ ] Ignore post of users already followed
- [ ] Finish tests


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


## Instalation

`pip install -r requirements.txt`


## Configuration

Provide credentials in the `config.yaml` and tune it at will.


## Usage

| Command | Description |
| --- | --- |
| `make init` | Initializes webdriver and creates a new conf based on the default one |
| `make run-bot` | Starts runing bot |


We told you it was easy.
