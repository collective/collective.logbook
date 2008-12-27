# -*- coding: utf-8 -*-
#
# File: utils.py
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

__author__    = 'Ramon Bartl <ramon.bartl@inquant.de>'
__docformat__ = 'plaintext'

import re

REGEX = re.compile(r'0x[0-9a-fA-F]+')


def hexfilter(text):
    """ unify hex numbers
    """
    return REGEX.sub('0x0000000', text)


def filtered_error_tail(error):
    """ last 5 lines of traceback with replaced oid's
    """
    tb_text = error.get('tb_text', '')
    tail = tb_text.splitlines()[-5:]
    filtered_tail = map(hexfilter, tail)
    return filtered_tail

# vim: set ft=python ts=4 sw=4 expandtab :
