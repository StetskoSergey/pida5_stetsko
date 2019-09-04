# Generated by Django 2.2.4 on 2019-08-21 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_delete_companyusers'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Company')),
                ('user_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
