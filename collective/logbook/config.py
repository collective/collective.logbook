# -*- coding: utf-8 -*-

import re
import logging

PACKAGENAME = "collective.logbook"

LOGGER = logging.getLogger(PACKAGENAME)
LOGLEVEL = "info"

# Regular expression to match the hex values of tracebacks
HEX_REGEX = re.compile(r'0x[0-9a-fA-F]+')

# 0 - all errors get saved in the log
#     (WARNING: this might cause an NotifyTraceback event flooding)
#
# 1 - references existing errors
REFERENCE_ERRORS = 1

# used for annotation storage
STORAGE_KEY = "LOGBOOK"
INDEX_KEY = "REFINDEX"
