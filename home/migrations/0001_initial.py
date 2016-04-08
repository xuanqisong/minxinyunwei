# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Homelist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('homename', models.CharField(max_length=256, verbose_name=b'\xe6\x93\x8d\xe4\xbd\x9c\xe9\xa1\xb9')),
                ('homeurl', models.CharField(max_length=256, verbose_name=b'\xe8\xbf\x9e\xe6\x8e\xa5\xe5\x9c\xb0\xe5\x9d\x80')),
                ('nav_display', models.BooleanField(default=False, verbose_name=b'\xe5\xaf\xbc\xe8\x88\xaa\xe6\x98\xbe\xe7\xa4\xba')),
                ('home_display', models.BooleanField(default=False, verbose_name=b'\xe9\xa6\x96\xe9\xa1\xb5\xe6\x98\xbe\xe7\xa4\xba')),
            ],
            options={
                'ordering': ['homename'],
                'verbose_name': '\u9996\u9875',
                'verbose_name_plural': '\u9996\u9875',
            },
        ),
    ]
