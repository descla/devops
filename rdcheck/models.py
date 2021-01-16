from django.db import models
from inventory.models import t_hosts

# Create your models here.
class t_result(models.Model):
    ip = models.ForeignKey(t_hosts, on_delete=models.CASCADE)
    ts = models.DateTimeField('ts', auto_now=True)
    metirc = models.JSONField('metric', null=True)
    ext = models.JSONField('ext', null=True)

    def __str__(self):
        return '_'.join(self.ip, self.ts)
