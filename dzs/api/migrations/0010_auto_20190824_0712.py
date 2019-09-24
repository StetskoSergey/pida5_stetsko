# Generated by Django 2.2.4 on 2019-08-24 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20190824_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outputid',
            name='debitor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Debitor'),
        ),
        migrations.AlterField(
            model_name='outputid',
            name='dogovor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Dogovor'),
        ),
        migrations.AlterField(
            model_name='outputid',
            name='ob_rash',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ObRash'),
        ),
    ]