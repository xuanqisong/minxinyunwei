from django.db import models


class Models(models.Model):
    #
    class Meta:
        permissions = (
            ("Use", "use"),
            ("Change", "Change"),
            ("Delete", "delete"),
            ("New", "new"),
            ("Show", "show"),
        )
