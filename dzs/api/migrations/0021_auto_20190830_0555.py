# Generated by Django 2.2.4 on 2019-08-30 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20190830_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debitor',
            name='f_adress',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='debitor',
            name='telef',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='debitor',
            name='u_adress',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
