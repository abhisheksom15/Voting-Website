# Generated by Django 2.1.7 on 2020-09-29 21:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0012_auto_20200930_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobileotp',
            name='Time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 30, 3, 9, 31, 915644)),
        ),
        migrations.AlterField(
            model_name='web_pages',
            name='page_text',
            field=models.CharField(max_length=5000),
        ),
    ]
