# Generated by Django 3.0.6 on 2020-06-17 14:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200617_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
