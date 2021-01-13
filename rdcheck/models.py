from django.db import models


# Create your models here.


class t_db_schema(models.Model):
    schema_choice = (
        ('db', 'db'),
        ('dg', 'dg'),
        ('rac', 'rac'),
        ('pri', 'pri'),
        ('std', 'std'),
    )
    schema = models.CharField("schema", choices=schema_choice, max_length=8)

class t_app(models.Model):
    app_name = models.CharField("name", max_length=32, blank=True, null=True)
    app_level = models.CharField("level", max_length=2, blank=True, null=True)

class t_hosts(models.Model):
    os_choice = (
        ("linux", "linux"),
        ("aix", "aix"),
        ("windows", "windows"),
    )
    db_choice = (
        ('oracle', 'oracle'),
        ('informix', 'informix'),
        ('db2', 'db2'),
        ('mysql', 'mysql'),
    )
    location = models.CharField("loc", max_length=10, blank=True, null=True)
    ip = models.CharField("ip", max_length=20, blank=True, null=False, unique=True)
    is_rdcheck = models.BooleanField("is_rdcheck", blank=False, null=True)
    os_type = models.CharField("os_type", choices=os_choice, max_length=16, blank=True, null=True)
    os_version = models.CharField('version', max_length=32, blank=True, null=True)
    device = models.CharField('device', max_length=1, blank=True, null=True)
    db_type = models.CharField("db_type", choices=db_choice, max_length=16, blank=True, null=True)
    db_schema = models.ForeignKey(t_db_schema, on_delete=models.CASCADE)
    hostname = models.CharField('hostname', max_length=32, blank=True, null=True)
    app = models.ForeignKey(t_app, on_delete=models.CASCADE)
    ts = models.DateTimeField('ts', auto_now=True)

    class Meta:
        app_label = 'hosts'
        db_table = "t_hosts"
        verbose_name = "主机表"

    def __str__(self):
        return '_'.join([self.ip, "主ip"])
