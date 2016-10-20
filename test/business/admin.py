#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from business import models
# Register your models here.

class Businessadmin(admin.ModelAdmin):
    list_display =('name','nic_name','site_type','status','front_urls','backend_urls','backend_allow_list')

class Bugsadmin(admin.ModelAdmin):
    list_display =('bug_type','bug_name','bug_status','bug_level','issue_description','resolution_step')

admin.site.register(models.Business,Businessadmin)
admin.site.register(models.Bugs,Bugsadmin)