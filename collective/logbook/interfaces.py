# -*- coding: utf-8 -*-
#
# File: interfaces.py
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

from zope.interface import Interface
from zope.interface import Attribute


class ILogBook(Interface):
    """ The LogBook API
    """

    error_count = Attribute(u"number of logged errors")
    reference_count = Attribute(u"number of referenced logged errors")
    saved_errors = Attribute(u"Saved Errors in storage")

    def error_log():
        """ zope error log object
        """

    def error(err_id):
        """ get the error object by id
        """

    def save_error(err_id):
        """ save the error to the storage
        """

    def delete_error(err_id):
        """ delete error from storage
        """

    def delete_all_errors():
        """ flush the logbook storage
        """

    def delete_all_references():
        """ flush the logbook reference storage
        """

    def search_error(err_id):
        """ search error by id
        """


class ILogBookStorage(Interface):
    """ The Logbook Storage
    """

    error_count = Attribute(u"number of logged errors")
    reference_count = Attribute(u"number of referenced logged errors")

    def save_error(error):
        """ save error to storage
        """

    def delete_error(err_id):
        """ delete error from storage by id
        """

    def get_error(err_id):
        """ get error by id, for error references return their referred error
        """

    def get_all_errors():
        """ get all errors
        """

    def get_counter(err_id):
        """ get the count of referenced errors
        """

    def get_referenced_errordata(err_id):
        """ get data for referenced errors
        """

    def delete_all_errors():
        """ delete all errors
        """

    def delete_all_references():
        """ delete all referenced errors
        """


class IErrorRaisedEvent(Interface):
    """ An Error occured
    """


class INotifyTraceback(Interface):
    """ An Error occured -> notify
    """

# vim: set ft=python ts=4 sw=4 expandtab :
