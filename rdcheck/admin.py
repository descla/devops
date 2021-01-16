from django.contrib import admin

# Register your models here.

from . import models

admin.site.register([models.t_hosts,models.t_app,models.t_db_schema])
