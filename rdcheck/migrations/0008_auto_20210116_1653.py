# Generated by Django 3.1.4 on 2021-01-16 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rdcheck', '0007_auto_20210116_1652'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='t_db_schema',
            options={},
        ),
        migrations.AlterField(
            model_name='t_db_schema',
            name='schema',
            field=models.CharField(choices=[('db', 'db'), ('dg', 'dg'), ('rac', 'rac'), ('single', 'single')], max_length=8, unique=True, verbose_name='模式'),
        ),
        migrations.AlterField(
            model_name='t_hosts',
            name='db_schema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdcheck.t_db_schema', verbose_name='数据库模式'),
        ),
    ]
