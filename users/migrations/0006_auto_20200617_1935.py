# Generated by Django 3.0.6 on 2020-06-17 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200617_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default1.jpg', upload_to='profile_pics/'),
        ),
    ]
