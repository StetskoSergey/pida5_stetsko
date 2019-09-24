# Generated by Django 2.2.4 on 2019-08-30 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20190828_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=150)),
                ('bic', models.CharField(db_index=True, max_length=10, unique=True)),
            ],
            options={
                'ordering': ['bic'],
            },
        ),
        migrations.RemoveField(
            model_name='debitor',
            name='t_type',
        ),
        migrations.AddField(
            model_name='debitor',
            name='f_adress',
            field=models.CharField(blank=True, db_index=True, max_length=150),
        ),
        migrations.AddField(
            model_name='debitor',
            name='telef',
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
        migrations.AddField(
            model_name='debitor',
            name='u_adress',
            field=models.CharField(db_index=True, default=None, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='debitor',
            name='ur_type',
            field=models.CharField(blank=True, choices=[('ЮрЛицо', 'Юридическое лицо'), ('ФизЛицо', 'Физическое лицо'), ('НР', 'Нерезидент'), ('ИП', 'Индивидуальный предприниматель')], db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='debitor',
            name='ur_forma',
            field=models.CharField(blank=True, choices=[('ОАО', 'Открытое акционерное общество'), ('ООО', 'Общество с ограниченной ответственностью'), ('ЗАО', 'Закрытое акционерное общество'), ('ИП', 'Индивидуальный предприниматель'), ('НР', 'Нерезидент')], db_index=True, max_length=50),
        ),
        migrations.CreateModel(
            name='Schet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_scheta', models.CharField(db_index=True, max_length=40)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Bank')),
                ('vlad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Debitor')),
            ],
            options={
                'ordering': ['n_scheta'],
            },
        ),
    ]