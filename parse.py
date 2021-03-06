#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from docopt import docopt
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager

import logging
import os
import sys
import subprocess


tmp_path = "/tmp/host_list"
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',)
logger = logging.getLogger(__name__)
__version__ = "0.1.0"
__doc__ = """
%(self_name)s

Parse ansible inventory files/directories to ssh config

Usage:
  %(self_name)s [--header=<FILE>] [--output=<FILE>] [--verbose] [--indent=<INDENT>] INVENTORY...
  %(self_name)s -h | --help
  %(self_name)s -V | --version

Options:
  -h --help                 Show this screen.
  -V --version              Show version.
  -v --verbose              Debug.
  -o=FILE --output=<FILE>   Save output as file.
  -H=FILE --header=<FILE>   Load custom header. [default: header]
  -i --indent=<SPACE>       Indent. [default: 2]
""" % dict(self_name=os.path.basename(__file__))


def main(args):
    host_list = []
    for inv in args.get("INVENTORY"):
        if not os.path.exists(inv):
            logger.error("Inventory file(s) not exist.")
            sys.exit(1)
        if os.path.isdir(inv):
            host_list.append(inv + "/*")
        else:
            host_list.append(inv)

    logger.debug(host_list)
    subprocess.call("cat %s > %s" % (" ".join(host_list), tmp_path), shell=True)

    header_path = args.get("--header")
    if os.path.exists(header_path):
        header = open(header_path, "r").read()
    else:
        header = None
        logger.warn("No custom header file found.")

    indent = " " * int(args.get("--indent"))

    logger.debug(header)
    output = "" + header if header else ""
    variable_manager = VariableManager()
    loader = DataLoader()
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=tmp_path)

    for host in inventory.get_hosts():
        host_all_vars = host.get_vars()
        host_all_vars.update(host.get_group_vars())
        output += "Host %s\n" % host.get_name()
        output += "%sHostname %s\n" % (indent, host.address)
        custom_user = False

        for user in ("ansible_ssh_user", "ansible_user"):
            if user in host_all_vars:
                output += "%sUser %s\n" % (indent, host_all_vars[user])
                custom_user = True
        if not custom_user:
            output += "%sUser root\n" % indent

        for port in ("ansible_ssh_port", "ansible_port"):
            if port in host_all_vars:
                output += "%sPort %d\n" % (indent, host_all_vars[port])

        output += "\n"

    if args.get("--output"):
        with open(args.get("--output"), "w") as f:
            f.writelines(output)
    else:
        print(output)


if __name__ == "__main__":
    args = docopt(__doc__, argv=sys.argv[1:], help=True, version=__version__, options_first=False)
    if args.get("--verbose"):
        logger.level = logging.DEBUG

    logger.debug(args)
    main(args)
