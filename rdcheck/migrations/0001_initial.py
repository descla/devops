# Generated by Django 3.1.4 on 2020-12-29 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='linux_res',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=20, verbose_name='ip')),
                ('os_type', models.CharField(blank=True, max_length=8, null=True, verbose_name='os_type')),
                ('flag', models.IntegerField(blank=True, null=True, verbose_name='flag')),
                ('ts', models.DateTimeField(null=True, verbose_name='ts')),
                ('metric', models.JSONField(verbose_name='metric')),
                ('ext', models.JSONField(verbose_name='ext')),
                ('gmt_create', models.JSONField(verbose_name='gmt_create')),
            ],
            options={
                'verbose_name': 'linux巡检结果',
                'db_table': 't_linux_rdcheck',
            },
        ),
    ]