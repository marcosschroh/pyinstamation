import sys
import signal
import argparse
import logging
from functools import partial

from pyinstamation.config import CONFIG, load_config
from pyinstamation.controller import Controller
from pyinstamation.bot import InstaBot
from pyinstamation.scrapper import InstaScrapper

logger = logging.getLogger(__name__)


def get_parser():
    description = (
        'Pyinstamation is an easy to use, config oriented, instagram bot, '
        'written in python 3.\n'
        'Please be sure that the configuration YAML matches '
        'your requirements.\n'
        'Some settings can be passed as arguments to avoid writing them '
        'in the config.yaml'
    )

    formater = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(prog='pyinstamation',
                                     description=description,
                                     formatter_class=formater)
    parser.add_argument('-u', '--username',
                        default=CONFIG.get('username', None),
                        help='instagram username')
    parser.add_argument('-p', '--password', help='instagram user password')
    parser.add_argument('-c', '--config', help='configuration file path')
    parser.add_argument('-H', '--hide_browser',
                        action="store_true", default=False,
                        help='dont show the browser, useful to run in servers')
    return parser


def signal_handler(bot, controller, signal, frame):
    logger.info('Aborted...')
    controller.set_stats(bot)
    logger.info('Saving stats!')
    bot.logout()
    sys.exit(0)


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.config is not None:
        load_config(filepath=args.config)

    scrapper = InstaScrapper(hide_browser=args.hide_browser)
    bot = InstaBot(scrapper, username=args.username, password=args.password)
    c = Controller(username=args.username)
    signal.signal(signal.SIGINT, partial(signal_handler, bot, c))
    c.run(bot)


if __name__ == '__main__':
    main()
