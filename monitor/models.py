# -*- coding: utf-8 -*-
from django.db import models


class Monitor(models.Model):
    #
    class Meta:
        permissions = (
            ("Use", "use"),
            ("Change", "change"),
            ("Delete", "delete"),
            ("Show", "show"),
            ("New", "new"),
        )
