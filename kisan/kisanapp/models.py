# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _


class ClimateHistory(TimeStampedModel):
    TEMP_TYPE_CHOICES = (
        ('Tmax', 'Tmax'),
        ('Tmin', 'Tmin'),
        ('Tmean', 'Tmean'),
        ('Sunshine', 'Sunshine'),
        ('Rainfall', 'Rainfall'),
        ('Raindays1mm', 'Raindays1mm'),
        ('AirFrost', 'AirFrost')
    )

    MONTH_AND_TYPE_CHOICES = (
        ('JAN', 'JAN'),
        ('FEB', 'FEB'),
        ('MAR', 'MAR'),
        ('APR', 'APR'),
        ('MAY', 'MAY'),
        ('JUN', 'JUN'),
        ('JUL', 'JUL'),
        ('AUG', 'AUG'),
        ('SEP', 'SEP'),
        ('OCT', 'OCT'),
        ('NOV', 'NOV'),
        ('DEC', 'DEC'),
        ('WIN', 'WIN'),
        ('SPR', 'SPR'),
        ('SUM', 'SUM'),
        ('AUT', 'AUT'),
        ('ANN', 'ANN')
    )

    YEAR_CHOICES = []
    for r in range(1900, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    region = models.CharField(max_length=100)
    temp_type = models.CharField(choices=TEMP_TYPE_CHOICES, max_length=100)
    month_and_type = models.CharField(choices=MONTH_AND_TYPE_CHOICES, max_length=100)
    year = models.IntegerField(_('year'), choices=YEAR_CHOICES)
    value = models.FloatField(null=True)
    category = models.CharField(max_length=500)

