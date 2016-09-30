#!/usr/bin/env python
from argparse import ArgumentParser
import json
from os import path
import sys

from rtmbot import RtmBot


slack_client = None


def rtm_bot(config):
    global slack_client
    bot = RtmBot(config)
    slack_client = bot.slack_client
    return bot


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Full path to config file.',
        metavar='path'
    )
    return parser.parse_args()


def get_config():
    f_name = 'rtmbot'

    json_name = '{}.json'.format(f_name)
    yaml_name = '{}.conf'.format(f_name)

    if path.exists(json_name):
        with open(json_name, 'r') as f:
            config = json.load(f)
    elif path.exists(yaml_name):
        import yaml

        args = parse_args()
        config = yaml.load(open(args.config or yaml_name, 'r'))
    else:
        config = {}


def main():
    # load args with config path
    try:
        bot = rtm_bot(get_config())
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == 'main':
    main()
