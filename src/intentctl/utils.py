# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import
#
# Copyright (c) 2018 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.

# Utility methods for the intentctl command

import json
import os
import sys


# Borrowed from the subscription-manager cli script
def system_exit(code, msgs=None):
    """Exit with a code and optional message(s). Saved a few lines of code."""

    if msgs:
        if type(msgs) not in [type([]), type(())]:
            msgs = (msgs, )
        for msg in msgs:
            sys.stderr.write(str(msg) + '\n')
    sys.exit(code)


def create_dir(path):
    """
    Attempts to create the path given (less any file)
    :param path: path
    :return: True if changes were made, false otherwise
    """
    try:
        os.makedirs(path, mode=0o755)
    except OSError as e:
        if e.errno == os.errno.EEXIST:
            # If the directory exists no changes necessary
            return False
        if e.errno == os.errno.EACCES:
            system_exit(os.EX_NOPERM,
                        'Cannot create directory {}\nAre you root?'.format(path))
    return True


def create_file(path, contents):
    """
    Attempts to create a file, with the given contents
    :param path: The desired path to the file
    :param contents: The contents to write to the file, should json-serializable
    :return: True if the file was newly created, false otherwise
    """
    try:
        with open(path, 'w') as f:
            if contents:
                json.dump(contents, f)
            f.flush()
    except OSError as e:
        if e.errno == os.errno.EEXIST:
            # If the file exists no changes necessary
            return False
        if e.errno == os.errno.EACCES:
            system_exit(os.EX_NOPERM, "Cannot create file {}\nAre you root?".format(path))
        else:
            raise
    return True
