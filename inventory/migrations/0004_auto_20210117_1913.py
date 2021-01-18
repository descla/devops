# Generated by Django 3.1.4 on 2021-01-17 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20210116_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_hosts',
            name='db_schema',
            field=models.CharField(blank=True, choices=[('db', 'db'), ('dg', 'dg'), ('rac', 'rac'), ('single', 'single'), (None, '无')], max_length=16, null=True, verbose_name='数据库模式'),
        ),
        migrations.AlterField(
            model_name='t_hosts',
            name='is_rdcheck',
            field=models.BooleanField(choices=[(True, '是'), (False, '否')], default=True, verbose_name='是否巡检'),
        ),
    ]