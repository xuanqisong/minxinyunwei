from django.db import models


# Create your models here.
class Script(models.Model):
    #
    class Meta:
        permissions = (
            ("Use", "use"),
            ("Change", "change"),
            ("Delete", "delete"),
            ("New", "new"),
            ("Show", "show"),
        )
