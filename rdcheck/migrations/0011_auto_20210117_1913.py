# Generated by Django 3.1.4 on 2021-01-17 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdcheck', '0010_auto_20210116_1852'),
    ]

    operations = [
        migrations.RenameField(
            model_name='t_linux_result',
            old_name='metirc',
            new_name='metric',
        ),
        migrations.RemoveField(
            model_name='t_linux_result',
            name='ext',
        ),
        migrations.AddField(
            model_name='t_linux_result',
            name='hostname',
            field=models.CharField(max_length=32, null=True, verbose_name='hostname'),
        ),
    ]