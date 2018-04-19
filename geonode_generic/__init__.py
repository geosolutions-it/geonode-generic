# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from datetime import datetime

from .celeryapp import app as celery_app

__all__ = ['celery_app']

def populate_service_last_check():
    from geonode.contrib.monitoring.models import Service
    # populate empty service.last_check for better collection
    for s in Service.objects.all():
        if not s.last_check:
            s.last_check = datetime.now()
            s.save()


def autoconfigure_monitoring(*args, **kwargs):
    from geonode.contrib.monitoring.models import Service, do_autoconfigure
    # run autoconfigure only if there are no services defined
    if not Service.objects.all():
        do_autoconfigure()
    populate_service_last_check()

class GenericGeonodeConfig(AppConfig):
    name = 'geonode_generic'
    verbose_name = 'Generic GeoNode'

    def ready(self):
        super(GenericGeonodeConfig, self).ready()
        if settings.MONITORING_ENABLED:
            post_migrate.connect(autoconfigure_monitoring, sender=self)


default_app_config = 'geonode_generic.GenericGeonodeConfig'
