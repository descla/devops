from django.db import models
from inventory.models import t_hosts


# Create your models here.
class t_linux_result(models.Model):
    ip = models.ForeignKey(t_hosts, on_delete=models.CASCADE)
    ts = models.DateTimeField('ts', auto_now=True)
    hostname = models.CharField('hostname', max_length=32, null=True)
    metric = models.JSONField('metric', null=True)

    def __str__(self):
        return str(self.ip)

    class Meta:
        verbose_name = 'linux巡检结果'
        verbose_name_plural = 'linux巡检结果'


