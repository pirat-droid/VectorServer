# Generated by Django 3.0.7 on 2020-08-01 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server_monit', '0004_auto_20200731_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storagemodel',
            name='raid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='server_monit.RAIDModel', verbose_name='RAID массив'),
        ),
    ]
