# Generated by Django 3.0.7 on 2020-07-31 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_monit', '0002_auto_20200731_1738'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storagemodel',
            old_name='serial',
            new_name='serial_number',
        ),
    ]
