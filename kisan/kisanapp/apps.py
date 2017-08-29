# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
import parser


class KisanappConfig(AppConfig):
    name = 'kisanapp'

    def ready(self):
        print('Ranvijay....')
        parser.start()
