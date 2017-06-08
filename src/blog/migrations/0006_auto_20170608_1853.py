# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import blog.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_auto_20170608_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.upload_location, width_field='width_field', height_field='height_field'),
        ),
    ]
