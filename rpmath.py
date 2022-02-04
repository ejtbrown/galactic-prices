#!/usr/bin/env python3
"""
rpmath.py - math parser for tabletop role play games, for processing things
            like "1d6 + 1d4 + 5" into a final value

Authors:
  Erick Brown

Copyright:
  2022, Erick Brown

Warranty:
  None - use this software at your own risk!
"""

import re
import random
import sys

re_dice = re.compile(r'[0-9]+d[0-9]+')
re_check = re.compile(r'[^0-9 +*/()-]')


def parse(raw_in, debug=False):
    """
    parse - parses an input string like "1d20 + 5" into a final value

    :param raw_in:      String to be parsed
    :type raw_in: str
    :param debug:       If True, debug messages will be output to stderr
    :type debug: bool
    :return:            Returns final value
    :rtype: float
    """

    working = raw_in
    if debug:
        sys.stderr.write("Starting with: '" + working + "'\n")

    # Roll whatever dice expressions are present
    while True:
        match = re_dice.search(working)
        if match is None:
            if debug:
                sys.stderr.write("No more dice\n")
            break

        to_roll = match.group(0).split('d')
        if debug:
            sys.stderr.write("Found dice: '" + 'd'.join(to_roll) + "'\n")

        result = 0
        for i in range(0, int(to_roll[0])):
            this_die = random.randint(1, int(to_roll[1]))
            result += this_die
            if debug:
                sys.stderr.write("Rolled " + str(this_die) + " on d" + to_roll[1] + "\n")

        if debug:
            sys.stderr.write("Result of " + 'd'.join(to_roll) + " is " + str(result) + "\n")

        working = working.replace('d'.join(to_roll), str(result), 1)
        if debug:
            sys.stderr.write("Working is now: '" + working + "'\n")

    # Make sure that there isn't anything untoward lurking in the expression
    if re_check.search(working):
        raise ValueError("One or more illegal characters in expression '" + working + "'")

    return eval(working)
