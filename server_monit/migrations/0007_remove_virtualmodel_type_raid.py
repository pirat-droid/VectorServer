# Generated by Django 3.0.7 on 2020-08-10 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_monit', '0006_auto_20200801_0538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='virtualmodel',
            name='type_raid',
        ),
    ]