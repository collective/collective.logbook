collective.logbook
==================

:Author: Ramon Bartl
:Version: 0.9.0

``collective.logbook`` add-on provides advanced persistent error logging for the
`open source Plone CMS <http://plone.org>`_.

.. contents:: Table of Contents
   :depth: 2


Lastest Build Status
--------------------

Master Branch https://github.com/collective/collective.logbook

.. image:: https://api.travis-ci.org/collective/collective.logbook.png?branch=master
    :target: https://travis-ci.org/collective/collective.logbook
    :alt: Build Status


Introduction
------------

For anonymous users Plone generates an Error Page, which contains an error
number. But what to do with this error number?

You have to log into your plone site, go to the ZMI, check the error_log object
and probably construct the url by hand to get the proper error with this error
number, e.g.:

http://localhost:8080/Plone/error_log/showEntry?id=1237283091.10.529903983894

If you are lucky, you will find the error by this number for further
investigation. If not, then maybe number of occured errors have exceeded the
number of exceptions to keep, or you are on the wrong Zope instance if you run a
cluster setup with a ZEO server, or maybe the Zope instance was restarted in
between, which caused a reset of all logged errors.

Not really smooth this behaviour.

Would it not be better to have a *nice frontend* where you can paste the error
number to a field and search for it? Keep all logged error messages
*persistent*, also when Zope restarts? Keep only *unique errors* and not a
thousand times the same Error? Get an *email notification* when a new, unique
error occured, so that you know already what's going on before your client mails
this error number to you?

If you think that this would be cool, `collective.logbook` is what you want.


Quickstart
----------

After installation, you can configure your logbook settings in the controlpanel:

http://localhost:8080/Plone/@@logbook-controlpanel

All occured errors get listed in the logbook view:

http://localhost:8080/Plone/@@logbook

As the logbook view diplays real errors that occured in your Plone site, it will
probably be empty at the first time.

To raise an error by intent, `collective.logbook` ships with two URL routes,
that do this job for you for testing purpose:

http://localhost:8080/Plone/@@error-test

This will raise an expected `RuntimeError`, which should be logged in the
logbook view. Calling this URL multiple times, should reference the error,
because of the same error signature.

This means, if you have configured Email notification, you will just be notified
once. The same is true for the webhooks, which will be described later.

To simulate different errors, you can browse this URL:

http://localhost:8080/Plone/@@random-error-test

This raises different errors, and multiple calls to this URL fills up the
logbook view with the occured errors, sorted by the most often happened errors
or to be more precisely, the errors that are referenced most often appear first.


Web hooks
---------

`collective.logbook` provides ability to HTTP POST error message to any web
service when an error happens in Plone. This behavior is called a web hook.

Use cases

- `Showing Plone errors real-time in Skype chat <https://github.com/opensourcehacker/sevabot>`_

- `Routing errors to different websites and services via Zapier <https://zapier.com/>`_

In Site Setup > Logbook you can enter URLs where HTTP POST will be asynchronously
performed on a traceback. HTTP POST payload is an message from Logbook,
containing a link for further information.

.. note::

    Currently repeated errros (same traceback signature, which get referenced in
    logbook) are not POST'ed again. You will receive a message only once, unless
    you clear logbook contents in the @@logbook management view.


Installation
------------

These instructions assume that you already have a Plone buildout that's built
and ready to run.

Edit your buildout.cfg file and look for the eggs key in the instance section.
Add collective.logbook to that list. Your list will look something like this::

    eggs =
        ...
        collective.logbook

Run buildout.

Activate the add-on via Site Setup > Add ons.


Compatibility
-------------

This extension works with Plone 4 and Plone 5.


Browser Testing
---------------

With `collective.logbook` enabled, it is simple to see all errors occured in your Plone site::

    >>> portal = self.getPortal()
    >>> browser = self.getBrowser()
    >>> browser.addHeader('Authorization', 'Basic admin:secret')

Remember some URLs::

    >>> portal_url = portal.absolute_url()
    >>> logbook_controlpanel_url = portal_url + "/@@logbook-controlpanel"
    >>> logbook_test_error_url = portal_url + "/@@error-test"
    >>> logbook_url = portal_url + "/@@logbook"

Browse to the `@@logbook` view::

    >>> browser.open(logbook_url)
    >>> 'Congratulations, there are 0 Errors in your Plone Site!' in browser.contents
    True

Now lets create an error with the `@@error-test` view, which raises an expected `RuntimeError`::

    >>> browser.open(logbook_test_error_url)
    Traceback (most recent call last):
    ...
    HTTPError: HTTP Error 500: Internal Server Error

    >>> browser.open(logbook_url)
    >>> "There are 1 saved (unique) Tracebacks and 0 referenced Tracebacks" in browser.contents
    True

The same error will be referenced and not logged again::

    >>> browser.open(logbook_test_error_url)
    Traceback (most recent call last):
    ...
    HTTPError: HTTP Error 500: Internal Server Error

    >>> browser.open(logbook_url)
    >>> "There are 1 saved (unique) Tracebacks and 1 referenced Tracebacks" in browser.contents
    True

There is also a `@@random-error-test` view, which randomly selects different tracebacks for testing.

Logbook logging can be deactivated on purpose in the `@@logbook-controlpanel` view::

    >>> browser.open(logbook_controlpanel_url)
    >>> browser.getControl(name="form.widgets.logbook_enabled:list").value = []
    >>> browser.getControl(name="form.buttons.save").click()

Errors should not be logged anymore::

    >>> browser.open(logbook_test_error_url)
    Traceback (most recent call last):
    ...
    HTTPError: HTTP Error 500: Internal Server Error

    >>> browser.open(logbook_url)
    >>> "There are 1 saved (unique) Tracebacks and 1 referenced Tracebacks" in browser.contents
    True

Finally, we remove all errors::

    >>> browser.open(logbook_url)
    >>> browser.getControl(name="form.button.deleteall").click()
    >>> 'Congratulations, there are 0 Errors in your Plone Site!' in browser.contents
    True


Technical Details
-----------------

This section gives an overview how `collective.logbook` works.


SiteErrorLog Patch
~~~~~~~~~~~~~~~~~~

`collective.logbook` patches the raising method of
`Products.SiteErrorLog.SiteErrorLog`::

    from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog

    _raising = SiteErrorLog.raising

    def raising(self, info):
        enty_url = _raising(self, info)
        notify(ErrorRaisedEvent(self, enty_url))
        return enty_url

The patch fires an `ErrorRaisedEvent` event before it returns the enty_url. The
entry url is the link to the standard SiteErrorLog like:

    http://localhost:8080/Plone/error_log/showEntry?id=1237283091.10.529903983894

The patch gets _only_ then installed, when you install collective.logbook over
the portal_quickinstaller tool and removes the patch, when you uninstall it.

You can also deactivate the patch over the logbook configlet of the plone
control panel.


Log Storage
~~~~~~~~~~~

The default storage is an annotation storage on the plone site root::

    <!-- default storage adapter -->
    <adapter
        for="*"
        factory=".storage.LogBookStorage"
      />

The default storage adapter creates 2 PersistentDict objects in your portal.
One 'main' storage and one 'index' storage, which keeps track of referenced
errors.


The storage will be fetched via an adapter lookup. So the more specific
adapter will win. Maybe an SQL storage with SQLAlchemy would be nice here:)


Notify Event
~~~~~~~~~~~~

When a new unique error occurs, an INotifyTraceback event gets fired. An
email event handler is already registered with collective.logbook::

    <subscriber
        for=".interfaces.INotifyTraceback"
        handler=".events.mailHandler"
      />

This handler will email new tracebacks to the list of email adresses
specified in the logbook configlet of the plone control panel.


Configuration
~~~~~~~~~~~~~

collective.logbook now uses Plone 5's registry to store its configuration.
It has 3 configuration keys:

  - logbook.logbook_log_mails
  - logbook.logbook_large_site
  - logbook.logbook_webhook_urls

These properties take the values you enter in logbook configlet in the plone
control panel.

The first one is used to email new tracebacks to these email addresses.

The second one changes some behaviour for large sites.

The third one does an HTTP POST to some URLs when an error occurs.
