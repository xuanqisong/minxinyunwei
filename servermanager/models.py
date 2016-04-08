from django.db import models


# Create your models here.
class Servermanager(models.Model):
    #
    class Meta:
        permissions = (
            ("Use", "use"),
            ("New", "new"),
            ("Change", "change"),
            ("Delete", "delete"),
            ("Show", "show"),
        )
