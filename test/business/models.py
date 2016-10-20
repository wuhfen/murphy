#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models 
from accounts.models import CustomUser as User
from assets.models import Server
from uuidfield import UUIDField
import datetime


class Business(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    full_name = models.CharField(max_length=128, verbose_name=u"全名")
    name = models.CharField(max_length=64, blank=True, null=True,verbose_name=u"简称")
    nic_name = models.CharField(max_length=64, verbose_name=u"代号")
    SITE_TYPE_CHOICES = (
    ('old_site', u"老平台"),
    ('new_site', u"新平台"),
    )
    site_type = models.CharField(max_length=64,choices=SITE_TYPE_CHOICES, verbose_name=u"站点类型")
    created_site_date = models.DateTimeField(blank=True, auto_now=True,verbose_name=u"建站时间")
    functionary = models.ForeignKey(User, related_name=u"functionary",blank=True, null=True, verbose_name=u"负责人", )
    ds_contact = models.ForeignKey(User, related_name=u"ds_contact",blank=True, null=True, verbose_name=u"我司专员", )
    agent_contact = models.CharField(max_length=100,blank=True, null=True, verbose_name=u"客户联系人")
    agent_contact = models.CharField(max_length=100,blank=True, null=True, verbose_name=u"客户联系方式")
    SITE_STATUS_CHOICES = (
    ('0', u"正常运转"),
    ('1', u"维护升级"),
    ('2', u"迁移过渡"),
    ('3', u"停止运转"),
    )
    status = models.CharField(max_length=100,choices=SITE_STATUS_CHOICES,verbose_name=u"站点状态")
    status_update_date = models.DateTimeField(blank=True, auto_now=True, verbose_name=u"客户状态变更日期")

    front_proxy = models.ManyToManyField(Server, blank=True, related_name=u"front_proxy", verbose_name=u"前端代理")
    front_urls = models.CharField(max_length=100,blank=True, null=True, verbose_name=u"前端域名")
    front_drop_list = models.CharField(max_length=600,blank=True, null=True, verbose_name=u"前端黑名单")
    front_image_site = models.ManyToManyField(Server, blank=True,related_name=u"front_image_site", verbose_name=u"前端图片站")
    front_cdn = models.CharField(max_length=100,blank=True, null=True, verbose_name=u"前端cdn")
    front_high_protection = models.CharField(max_length=100,blank=True, null=True, verbose_name=u"前端高防")

    backend_proxy = models.ManyToManyField(Server, blank=True, related_name=u"backend_proxy",verbose_name=u"后台代理")
    backend_urls = models.CharField(max_length=300,blank=True, null=True, verbose_name=u"后台域名")
    backend_allow_list = models.CharField(max_length=100,blank=True, null=True, verbose_name=u"后台白名单")
    backend_image_site = models.ManyToManyField(Server, blank=True, related_name=u"backend_image_site", verbose_name=u"后台图片站")

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)
    class Meta:
        verbose_name = u'业务Business'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class Bugs(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    BUG_TYPE_CHOICES = (
    ('code_bug', u"代码bug"),
    ('intenet_bug', u"网络故障"),
    ('server_bug', u"服务器故障"),
    ('service_bug', u"应用服务故障"),
    ('preson_bug', u"误操作故障"),
    ('attack_bug', u"被攻击"),
    ('other_bug', u"其他"),
    )
    bug_type = models.CharField(max_length=64,choices=BUG_TYPE_CHOICES, verbose_name=u"故障类型")
    bug_name = models.CharField(max_length=64, verbose_name=u"故障名称")
    business = models.ManyToManyField(Business,blank=True,verbose_name=u"涉及业务")
    BUG_STATUS_CHOICES = (
    ('0', u"发现上报"),
    ('1', u"处理中"),
    ('2', u"已解决"),
    )
    bug_status = models.CharField(max_length=100,choices=BUG_STATUS_CHOICES,verbose_name=u"故障状态")
    BUG_LEVEL_CHOICES = (
    ('0', u"一般故障"),
    ('1', u"重要故障"),
    ('2', u"严重故障"),
    ('3', u"灾难故障"),
    )
    bug_level = models.CharField(max_length=100,choices=BUG_LEVEL_CHOICES,verbose_name=u"故障级别")
    bug_level_change = models.BooleanField(default=False, verbose_name=u"故障是否升级")
    appear_time = models.IntegerField(blank=True, null=True, verbose_name=u'出现次数')
    bug_assigned = models.ForeignKey(User, related_name=u"bug_assigned",blank=True, null=True, verbose_name=u"处理人员")
    bug_change_assigned = models.ForeignKey(User, related_name=u"bug_change_assigned",blank=True, null=True, verbose_name=u"转派人员")
    bug_tracker = models.ForeignKey(User, related_name=u"bug_tracker",blank=True, null=True, verbose_name=u"跟踪人员")
    bug_accept = models.BooleanField(default=False, verbose_name=u"是否接单")
    bug_assigned_change = models.BooleanField(default=False, verbose_name=u"是否转派")
    bug_solve = models.BooleanField(default=False, verbose_name=u"是否解决")
    issue_description = models.TextField(u'故障描述', null=True, blank=True)
    resolution_step = models.TextField(u'处理步骤', null=True, blank=True)
    change_reason = models.TextField(u'转派原因', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = u'故障Bugs'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.bug_name










