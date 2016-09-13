#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: test interface/call for sending container id back to RPC

from __future__ import unicode_literals
from docopt import docopt

import logging
import os
import sys


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',)
logger = logging.getLogger(__name__)
self_name = os.path.basename(__file__)
__version__ = "0.1.0"
__doc__ = """
%(self_name)s

Parse ansible inventory files/directories to ssh config

Usage:
  %(self_name)s [--output=<FILE>] [--verbose] INVENTORY...
  %(self_name)s -h | --help
  %(self_name)s -V | --version

Options:
  -h --help                 Show this screen.
  -V --version              Show version.
  -v --verbose              Debug
  -o=FILE --output=<FILE>   Save output as file
""" % dict(self_name=self_name,)


def main(args):
    """docstring for main"""
    output_file = args.get("--output")


if __name__ == "__main__":
    args = docopt(__doc__, argv=sys.argv[1:], help=True, version=__version__, options_first=False)
    if args.get("--verbose"):
        logger.level = logging.DEBUG

    logger.debug(args)
    main(args)
