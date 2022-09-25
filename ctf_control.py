#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
""" The main tool to run ctf challenges """

import argparse
import argcomplete
import signal
import time
import sys

from app.ctfcontrol import ChallengeControl


class ExitHandler:
    def __init__(self, challengecontrol):
        self.cc = challengecontrol
    def __call__(self, signo, frame):
        self.cc.stop()
        print("quitting")
        sys.exit(0)


def explain(args):  # pylint: disable=unused-argument
    """ Explain the tool"""

    print("Please specify a command to execute. For a list see <help>")


def run(challengecontrol):
    """ Run challenges

    @param challengecontrol
    """

    challengecontrol.run()




def create_parser():
    """ Creates the parser for the command line arguments"""
    lparser = argparse.ArgumentParser("Controls challenges on the configured systems")
    subparsers = lparser.add_subparsers(help="sub-commands")

    lparser.set_defaults(func=explain)
    lparser.add_argument('--verbose', '-v', action='count', default=0, help="Verbosity level")

    # Sub parser for machine creation
    parser_run = subparsers.add_parser("run", help="run challenges")
    parser_run.set_defaults(func=run)
    parser_run.add_argument("--configfile", default="ctf_config.yaml", help="Config file to create the challenge from")

    return lparser


if __name__ == "__main__":
    parser = create_parser()
    argcomplete.autocomplete(parser)
    arguments = parser.parse_args()
    challengecontrol = ChallengeControl(arguments.configfile, arguments.verbose)
    arguments.func(challengecontrol)
    signal.signal(signal.SIGINT, ExitHandler(challengecontrol))
    print("Systems up... CTRL-C to quit.")
    while True:
        time.sleep(1)
