# Generated by Django 4.2.4 on 2023-08-04 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jellyfishscore',
            name='beach_id',
        ),
    ]
