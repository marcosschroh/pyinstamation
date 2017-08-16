import argparse
from pyinstamation import CONFIG
from pyinstamation.bot import InstaBot
from pyinstamation.controller import Controller


def get_arguments():
    description = (
        'Pyinstamation is a bot with a lot of functionality to navigate Instagram.\n'
        'Please be sure that the configuration matches your requirements.\n'
        'Some settings can be passed as arguments to avoid writing them in the config.yaml'
    )

    formater = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(prog='pyinstamation', description=description,
                                     formatter_class=formater)
    parser.add_argument('-u', '--username', default=CONFIG.get('username', None),
                        help='instagram username')
    parser.add_argument('-p', '--password', help='instagram user password')
    parser.add_argument('-c', '--config', help='configuration file path')
    parser.add_argument('-s', '--silent', action="store_true", default=False,
                        help='do not log anything')
    return parser.parse_args()


def main():
    args = get_arguments()
    print(args)


if __name__ == '__main__':
    main()
