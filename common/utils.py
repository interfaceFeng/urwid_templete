# -*- coding: utf-8 -*-

import logging
import consts

log = logging.getLogger('utils')


def get_dsMenu_version(versionfile = consts.VERSION_FILE):
    try:
        with open(versionfile, 'r') as f:
            return f.read().strip()
    except IOError:
        log.error("set dsmenu version from %s fail" % versionfile)
        return ""