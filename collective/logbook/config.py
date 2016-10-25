# -*- coding: utf-8 -*-
#
# File: config.py
#
# Copyright (c) InQuant GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__ = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'

import logging

PACKAGENAME = "collective.logbook"

LOGGER = logging.getLogger(PACKAGENAME)

# 0 - all errors get saved in the log
#     (WARNING: this might cause an NotifyTraceback event flooding)
#
# 1 - references existing errors
REFERENCE_ERRORS = 1

# used for annotation storage
STORAGE_KEY = "LOGBOOK"
INDEX_KEY = "REFINDEX"

# vim: set ft=python ts=4 sw=4 expandtab :
