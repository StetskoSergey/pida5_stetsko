# Generated by Django 2.2.4 on 2019-08-26 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20190826_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='d_key',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='key',
            field=models.SlugField(max_length=100, null=True, unique=True),
        ),
    ]