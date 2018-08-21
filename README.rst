# Geonode Generic

GeoNode "materialized" project for vanilla GeoNode deployments - this is
[Kartoza's](http://kartoza.com) fork from the great work by 
[Geosolutions-it](https://github.com/geosolutions-it/geonode-generic).

## Backups:


Backups are made automatically each night.

Backups will be made in ``/mnt/volumes/backups``. Backups are made using the
[Geosolutions backup docker project](https://github.com/geosolutions-it/geonode-backup-docker). See
restoring backups section below.

## Restoring backups:

There is a restore container for restoring backups. This is based on [the
Geosolutions restore docker project](https://github.com/geosolutions-it/geonode-restore-docker).

See the backups section above for details of how the backups work,


## Setup with Rancher 1.6

Currently this repository supports setup through Rancher 1.6.
The catalog template is publicly available via the (Kartoza rancher catalogue)[]

You can load the template from Rancher UI or Rancher CLI and set the questions
/ variables defined in the Rancher compose file.

A standalone docker-compose will be reintroduced later.


## Configuration

**Note these original notes from GeoSolutions need review**

Since this application uses geonode, base source of settings is
``geonode.settings`` module. It provides defaults for many items, which are
used by geonode. This application has own settings module,
``geonode_generic.settings``, which includes ``geonode.settings``. It
customizes few elements: * static/media files locations - they will be
collected and stored along with this application files by default. This is
useful during development.  * Adds ``geonode_generic`` to installed
applications, updates templates, staticfiles dirs, sets urlconf to
``geonode_generic.urls``. 

Whether you deploy development or production environment, you should create
additional settings file. Convention is to make
``geonode_generic.local_settings`` module. It is recommended to use
``geonode_generic/local_settings.py``.. That file contains small subset of
settings for edition. It should:
 * not be versioned along with application (because changes you make for your private deployment may become public),
 * have customized at least``DATABASES``, ``SECRET_KEY`` and ``SITEURL``. 

You can add more settings there, note however, some settings (notably
``DEBUG_STATIC``, ``EMAIL_ENABLE``, ``*_ROOT``, and few others) can be used by
other settings, or as condition values, which change other settings. For
example, ``EMAIL_ENABLE`` defined in ``geonode.settings`` enables whole email
handling block, so if you disable it in your ``local_settings``, derived
settings will be preserved. You should carefully check if additional settings
you change don't trigger other settings.

To ilustrate the whole concept of chained settings:

```
    +------------------------+-------------+-------------------------------+-------------+----------------------------------+
    |  GeoNode configuration |             |   Your application default    |             |  (optionally) Your deployment(s) |
    |                        |             |        configuration          |             |                                  |
    +========================|=============|===============================|=============|==================================+
    |                        | included by |                               | included by |                                  |
    |   geonode.settings     |     ->      |  geonode_generic.settings    |      ->     |  geonode_generic.local_settings |
    +------------------------|-------------|-------------------------------|-------------|----------------------------------+
```
