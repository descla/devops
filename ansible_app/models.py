from django.db import models

# Create your models here.

class rdcheck_host(models.Model):
    ip = models.CharField("主IP", max_length=20, blank=True, null=False)
    os_type = models.CharField("操作系统", max_length=8, blank=True, null=False)
    app_name = models.CharField("应用名", max_length=20, blank=True, null=True)
    script_flag = models.IntegerField("脚本更新", blank=True, null=True)
    reason = models.CharField("巡检项", blank=True, null=True)
    ext = models.JSONField('ext')
    gmt_create = models.DateTimeField('gmt_create', blank=True, null=True)

    class Meta:
        app_label = "主机管理"
        db_table = "t_inventory"
        verbose_name = "inventory"
    def __str__(self):
        return '_'.join([self.ip, "主ip"])


