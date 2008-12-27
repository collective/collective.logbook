Introduction
============

Advanced Error Logging for Plone.


Motivation
----------

- Why not use the Site Error Log?

  The standard Site Error Log forgets all logs after restart

  There is no search form to search errors by ID

  Only accessible throug ZMI

  It is not possible to save unique errors

  Not possible to get an event, e.g. Email notification, if a new (unique)
  error occurs.


- Why use collective.logbook?

  Keeps all logs persistent, also after Zope restarts

  Keeps only unique errors and references new errors to existing errors (if
  they exist, of course)

  Search Errors by error number

  Nice Front End

  Comes with an RSS and ATOM feed

  You can write a custom event handler to get informed when a new (unique)
  error occur

  get an error count to see how often an error occured

  good tested (so far)

  transparent to Site Error Log


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


Usage
-----

Logbook:
http://localhost:8080/plone/@@logbook

RSS:
http://localhost:8080/plone/@@logbook_rss.xml

ATOM:
http://localhost:8080/plone/@@logbook_atom.xml


::
 vim: set ft=rst ts=4 sw=4 expandtab tw=78 :
