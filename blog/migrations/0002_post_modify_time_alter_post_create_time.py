# Generated by Django 4.0.1 on 2022-02-11 05:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='modify_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 11, 5, 53, 32, 85225, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 11, 5, 53, 32, 85225, tzinfo=utc)),
        ),
    ]