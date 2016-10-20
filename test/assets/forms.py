#!/usr/bin/env python
#coding:utf8
from assets import models
from django import forms
from django.forms import ModelForm

class AssetForm(ModelForm):
    FAVORITE_COLORS_CHOICES = (
        ('serverhost', u'物理机'),
        ('virtual', u'虚拟机'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('contain', u'Docker'),
        ('others', u'其它类'),
    )
    asset_number = forms.CharField(label=u'资产编号',widget=forms.TextInput(attrs={'placeholder': 'DT-server-20161014-001'}))
    asset_type = forms.CharField(label=u'资产类型',required=False,widget=forms.Select(attrs={'initial': 'serverhost','hidden': "hidden"}, choices=FAVORITE_COLORS_CHOICES))
    class Meta:
        model = models.Asset
        fields = '__all__'

class ServerForm(ModelForm):
    ssh_password = forms.CharField(label=u'SHH密钥',required=False,widget=forms.PasswordInput)
    class Meta:
        model = models.Server
        exclude = ['asset']


class CPUForm(ModelForm):
    class Meta:
        model = models.CPU
        fields = ["cpu_model","cpu_count","cpu_core_count","memo"]

class RAMForm(ModelForm):
    class Meta:
        model = models.RAM
        fields = ["model","capacity","sn","slot","memo"]

class DiskForm(ModelForm):
    class Meta:
        model = models.Disk
        fields = ["sn","slot","iface_type","model","manufactory","capacity","memo"]

class NICForm(ModelForm):
    macaddress = forms.CharField(label=u'MAC地址',required=True, widget=forms.TextInput(attrs={'placeholder': '必填项'}))
    class Meta:
        model = models.NIC
        fields = ["name","model","macaddress","ipaddress","netmask","memo"]