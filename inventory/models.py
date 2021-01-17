from django.db import models


# Create your models here.


# 应用的名称，简称， 等级
class t_app(models.Model):
    def __str__(self):
        return self.app_name

    app_name = models.CharField('应用名', max_length=32, primary_key=True)
    app_level = models.CharField('级别', max_length=2, blank=True, null=True)
    app_sname = models.CharField('英文简称', max_length=16, blank=True, null=True)

    class Meta:
        app_label = 'inventory'
        verbose_name = '应用表'
        verbose_name_plural = '应用表'


# 主机表
class t_hosts(models.Model):
    os_choice = (
        ('linux', 'linux'),
        ('aix', 'aix'),
        ('windows', 'windows'),
    )
    db_choice = (
        ('oracle', 'oracle'),
        ('informix', 'informix'),
        ('db2', 'db2'),
        ('mysql', 'mysql'),
        (None, '无'),
    )
    device_choice = (
        ('V', '虚拟机'),
        ('P', '物理机'),
    )
    schema_choice = (
        ('db', 'db'),
        ('dg', 'dg'),
        ('rac', 'rac'),
        ('single', 'single'),
        (None, '无'),
    )
    rdcheck_choice = (
        (True, '是'),
        (False, '否'),
    )
    location = models.CharField('loc', max_length=10, blank=True, null=True)
    ip = models.CharField('ip', max_length=20, blank=True, null=False, primary_key=True)
    is_rdcheck = models.BooleanField('是否巡检', choices=rdcheck_choice, blank=False)
    os_type = models.CharField('OS', choices=os_choice, max_length=16, blank=True, null=True)
    os_version = models.CharField('版本', max_length=32, blank=True, null=True)
    device = models.CharField('设备类型', choices=device_choice, max_length=16, blank=True, null=True)
    db_type = models.CharField('数据库', choices=db_choice, max_length=16, blank=True, null=True)
    db_schema = models.CharField('数据库模式', choices=schema_choice, max_length=16, blank=True, null=True)
    hostname = models.CharField('主机名', max_length=32, blank=True, null=True)
    app = models.ForeignKey(t_app, on_delete=models.CASCADE)
    ts = models.DateTimeField('时间', auto_now=True)

    class Meta:
        app_label = 'inventory'
        verbose_name = '主机表'
        verbose_name_plural = '主机表'

    def __str__(self):
        return '_'.join([self.ip, self.app.app_name])
