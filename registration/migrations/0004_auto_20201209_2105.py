# Generated by Django 3.1.4 on 2020-12-09 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20201209_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personmodel',
            name='style',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='registration.stylemodel', verbose_name='Класс'),
        ),
    ]
