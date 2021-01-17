from django.contrib import admin

# Register your models here.
from . import models



class Hosts_Admin(admin.ModelAdmin):
    list_display = ('location', 'ip', 'hostname', 'app', 'is_rdcheck', 'os_type', 'device', 'db_type')
    list_display_links = ('ip',)
    list_filter = ('location', 'is_rdcheck', 'os_type', 'device', 'db_type')
    search_fields = ['ip', 'app__app_name']
    list_editable = ['is_rdcheck']


class App_Admin(admin.ModelAdmin):
    list_display = ('app_name', 'app_level', 'app_sname')
    list_display_links = ('app_name',)
    search_fields = ['app_name', 'app_level']


admin.site.register(models.t_hosts, Hosts_Admin)
admin.site.register(models.t_app, App_Admin)
