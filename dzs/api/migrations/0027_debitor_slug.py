# Generated by Django 2.2.4 on 2019-08-30 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20190830_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='debitor',
            name='slug',
            field=models.SlugField(default=None, unique=True),
            preserve_default=False,
        ),
    ]
