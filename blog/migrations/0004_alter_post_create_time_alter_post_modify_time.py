# Generated by Django 4.0.1 on 2022-02-11 05:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_create_time_alter_post_modify_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='post',
            name='modify_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
