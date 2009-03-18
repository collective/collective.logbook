Introduction
============

Advanced persistent Error Logging for Plone.


Motivation
----------

Plone generates for anonymous users an Error Page which contains an error
number. But what to do with this error number?

You have to log into your plone site, go to the ZMI, check the error_log
object and probably construct the url by hand to get ther proper error with
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

No, you won't get DOOOOMED when you install collective.logbook:)


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
~~~~~~~~~~~~~

When a new unique error occurs, an INotifyTraceback event gets fired. An
email event handler is already registered with collective.logbook::

    <subscriber
        for=".interfaces.INotifyTraceback"
        handler=".events.mailHandler"
      />

This handler will email new tracebacks to the list of email adresses
specified in the logbook configlet of the plone control panel.


Properties
~~~~~~~~~~

collective.logbook installs 2 Properties in your application root:

  - logbook_enabled
  - logbook_log_mails

These properties take the values you enter in logbook configlet in the plone
control panel.

The first one checks if logbook logging is disabled or not when you restart
your instance::

    def initialize(context):
        """ Initializer called when used as a Zope 2 product. """

        app = context._ProductContext__app
        enabled = app.getProperty("logbook_enabled", False)

        if enabled:
            monkey.install_monkey()


The latter one is used to email new tracebacks to these email addresses.

The properties get uninstalled when you uninstall collective.logbook via the
quickinstaller tool.


Unit Tests
~~~~~~~~~~

There are some unit tests which can be run with::

    ./bin/instance test collective.logbook

    Running:
    ..............
    Ran 14 tests with 0 failures and 0 errors in 0.145 seconds.

more to come...


Usage
-----

After insall, go to http://your-plone-site/@@logbook


Installation
------------

These instructions assume that you already have a Plone 3 buildout that's built
and ready to run.

Edit your buildout.cfg file and look for the eggs key in the instance section.
Add collective.logbook to that list. Your list will look something like this::

    eggs =
        ${buildout:eggs}
        ${plone:eggs}
        collective.logbook

In the same section, look for the zcml key. Add collective.logbook here,
too::

    zcml = collective.logbook

::
 vim: set ft=rst ts=4 sw=4 expandtab tw=78 :
