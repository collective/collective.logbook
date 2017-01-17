# -*- coding: utf-8 -*-

import logging

PACKAGENAME = "collective.logbook"

LOGGER = logging.getLogger(PACKAGENAME)


# Gets True when the SiteErrorLog monkey patch gets applied
PATCH_APPLIED = False

# 0 - all errors get saved in the log
#     (WARNING: this might cause an NotifyTraceback event flooding)
#
# 1 - references existing errors
REFERENCE_ERRORS = 1

# used for annotation storage
STORAGE_KEY = "LOGBOOK"
INDEX_KEY = "REFINDEX"
