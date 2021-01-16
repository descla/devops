from django.db import models


# Create your models here.

# 数据库的模式
class t_db_schema(models.Model):
    def __str__(self):
        return self.schema

    schema_choice = (
        ('db', 'db'),
        ('dg', 'dg'),
        ('rac', 'rac'),
        ('single', 'single'),
    )
    schema = models.CharField("模式", choices=schema_choice, max_length=8, unique=True)


# 应用的名称，简称， 等级
class t_app(models.Model):
    def __str__(self):
        return self.app_name

    app_name = models.CharField("name", max_length=32, primary_key=True)
    app_level = models.CharField("level", max_length=2, blank=True, null=True)
    app_sname = models.CharField("sname", max_length=16, blank=True, null=True)


# 主机表
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
    device_choice = (
        ('V', '虚拟机'),
        ('P', '物理机'),
    )
    location = models.CharField("loc", max_length=10, blank=True, null=True)
    ip = models.CharField("ip", max_length=20, blank=True, null=False, primary_key=True)
    is_rdcheck = models.BooleanField("是否巡检", blank=False, null=True)
    os_type = models.CharField("OS", choices=os_choice, max_length=16, blank=True, null=True)
    os_version = models.CharField('版本', max_length=32, blank=True, null=True)
    device = models.CharField('设备类型', choices=device_choice, max_length=16, blank=True, null=True)
    db_type = models.CharField("数据库", choices=db_choice, max_length=16, blank=True, null=True)
    db_schema = models.ForeignKey(t_db_schema,verbose_name='数据库模式', on_delete=models.CASCADE)
    hostname = models.CharField('主机名', max_length=32, blank=True, null=True)
    app = models.ForeignKey(t_app, on_delete=models.CASCADE)
    ts = models.DateTimeField('时间', auto_now=True)

    # class Meta:
    #    app_label = 'hosts'
    #    db_table = "t_hosts"
    #    verbose_name = "主机表"

    def __str__(self):
        return '_'.join([self.ip, self.app.app_name])


class t_result(models.Model):
    ip = models.ForeignKey(t_hosts, on_delete=models.CASCADE)
    ts = models.DateTimeField('ts', auto_now=True)
    metirc = models.JSONField('metric', null=True)
    ext = models.JSONField('ext', null=True)

    def __str__(self):
        return '_'.join(self.ip, self.ts)
