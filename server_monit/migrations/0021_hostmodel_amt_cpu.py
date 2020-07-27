# Generated by Django 3.0.7 on 2020-07-23 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server_monit', '0020_remove_hostmodel_amt_cpu'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostmodel',
            name='amt_cpu',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='server_monit.CPUModel', verbose_name='Количество процессоров на материнской плате'),
        ),
    ]
