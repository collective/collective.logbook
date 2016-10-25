Introduction
------------


``collective.logbook`` add-on provides
advanced persistent error logging for `open source Plone CMS <http://plone.org>`_.

.. contents :: :local:

Installation
------------

These instructions assume that you already have a Plone 3 buildout that's built
and ready to run.

Edit your buildout.cfg file and look for the eggs key in the instance section.
Add collective.logbook to that list. Your list will look something like this::

    eggs =
        collective.logbook

Enable via Site Setup > Add ons.

Usage
-----

Settings
~~~~~~~~

See Site Setup for log book settings.

Inspecting errors
~~~~~~~~~~~~~~~~~~

After install, go to http://your-plone-site/@@logbook

The errors are logged there. You can tune some parameters.

Testing
~~~~~~~

``collective.logbook`` provides a view ``error-test`` which Site managers can access to
generate a test traceback.

First visit ``@@error-test`` and make sure the error appears in ``@@logbook`` view.

.. note ::

    You might need to turn on both Logbook enabled and Large site in Logbook Site Setup.
    This may be a bug regarding new Plone versions and production mode.

Web hooks
---------

``collective.logbook`` provides ability to HTTP POST
error message to any web service when an error happens in Plone.
This behavior is called a web hook.

Use cases

* `Showing Plone errors real-time in Skype chat <https://github.com/opensourcehacker/sevabot>`_

* `Routing errors to different websites and services via Zapier <https://zapier.com/>`_

In Site Setup > Logbook you can enter URLs where HTTP POST will be asynchronously
performed on a traceback. HTTP POST payload is an message from Logbook,
containing a link for further information.

.. note ::

    Currently repeated errros (same traceback signature) are not POST'ed again.
    You will receive message only once unless until you clear logbook contents in
    @@logbook management view.


Motivation
----------

For anonymous users Plone generates an Error Page which contains an error
number. But what to do with this error number?

You have to log into your plone site, go to the ZMI, check the error_log
object and probably construct the url by hand to get the proper error with
this error number, like::

    http://your-plone-site/error_log/showEntry?id=1237283091.10.529903983894

If you are lucky, you will find the error. If not, and the number of occured
errors exceeded the number of exceptions to keep, or maybe a cronjob restarted
your zope instance, then....

Hmm, not really smooth this behaviour.

Wouldn't it be better to have a nice frontend where you can paste the error
number to a field and search for it? Keep all log persistent, also when zope
restarts? Keep only unique errors and not thousand times the same Error? Get
an email when a new, unique error occured, so you know already what's going on
before your customer mails this error number to you?

If you think that this would be cool, collective.logbook is what you want:)


Under the Hood
--------------

No, you won't get DOOOOMED when you install collective.logbook :)


SiteErrorLog Patch
~~~~~~~~~~~~~~~~~~

collective.logbook patches the raising method of
Products.SiteErrorLog.SiteErrorLog::

    from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog

    _raising = SiteErrorLog.raising

    def raising(self, info):
        enty_url = _raising(self, info)
        notify(ErrorRaisedEvent(self, enty_url))
        return enty_url

The patch fires an 'ErrorRaisedEvent' event before it returns the enty_url.
The entry url is the link to the standard SiteErrorLog like::

    http://your-plone-site/error_log/showEntry?id=1237283091.10.529903983894

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

Unit Tests
~~~~~~~~~~

The product contains some unit tests.

more to come...

..
 vim: set ft=rst ts=4 sw=4 expandtab tw=78 :
