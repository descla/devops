from django.db import models

# Create your models here.

class linux_res(models.Model):
    ip = models.CharField("ip", max_length=20, blank=True, null=False)
    os_type = models.CharField("os_type", max_length=8, blank=True, null=True)
    flag = models.IntegerField("flag", blank=True, null=True)
    ts = models.DateTimeField('ts', null=True)
    metric = models.JSONField('metric')
    ext = models.JSONField('ext')
    gmt_create = models.DateTimeField('gmt_create', blank=True, null=True)

    class Meta:
        app_label = 'rdcheck'
        db_table = "t_linux_rdcheck"
        verbose_name = "linux巡检结果"
    def __str__(self):
        return '_'.join([self.ip, "主ip"])


