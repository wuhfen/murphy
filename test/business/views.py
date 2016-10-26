#!/usr/bin/env python
# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required, permission_required
# from forms import BusinessForm, BugsForm
from models import Business,Bugs,Platform,DomainName
from forms import BusinessForm, PlatfForm, DomainNameForm

from Allow_list.models import Iptables
from assets.models import Server
import time

##业务增删查改
@permission_required('business.Can_add_business', login_url='/auth_error/')
def business_list(request):
    business_data = Business.objects.all()
    return render(request,'business/business_list.html',locals())

@permission_required('business.Can_add_business', login_url='/auth_error/')
def business_delete(request,uuid):
    business_data = Business.objects.get(pk=uuid)
    business_data.delete()
    return render(request,'business/business_list.html',locals())


@permission_required('business.Can_add_business', login_url='/auth_error/')
def business_add(request):
    bf = BusinessForm()
    if request.method == 'POST':
        bf = BusinessForm(request.POST)
        if bf.is_valid():
            bf_data = bf.save()
            return HttpResponseRedirect('/allow/welcome/')
    return render(request,'business/business_add.html',locals())

@permission_required('business.Can_add_business', login_url='/auth_error/')
def business_edit(request,uuid):
    business = get_object_or_404(Business, uuid=uuid)
    status = business.status
    bf = BusinessForm(instance=business)
    if request.method == 'POST':
        bf = BusinessForm(request.POST,instance=business)
        new_status = request.POST.get('status', '')
        if bf.is_valid():
            status_change_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            bf_data = bf.save(commit=False)
            if status == new_status:
                bf_data.save()
            else:
                bf_data.status_update_date = status_change_time
                bf_data.save()
            return HttpResponseRedirect('/allow/welcome/')
    return render(request,'business/business_edit.html',locals())

@permission_required('business.Can_add_domainname', login_url='/auth_error/')
def business_detail(request,uuid):
    business_data = get_object_or_404(Business, uuid=uuid)
    return render(request,'business/business_detail.html',locals())

##业务平台增删查改
@permission_required('business.Can_add_business', login_url='/auth_error/')
def platform_list(request):
    platform_data = Platform.objects.all()
    return render(request,'business/platform_list.html',locals())

@permission_required('business.Can_add_business', login_url='/auth_error/')
def platform_add(request):
    pf = PlatfForm()
    if request.method == 'POST':
        pf = PlatfForm(request.POST)
        if pf.is_valid():
            pf_data = pf.save()
            return HttpResponseRedirect('/allow/welcome/')
    return render(request,'business/platform_add.html',locals())


@permission_required('business.Can_add_business', login_url='/auth_error/')
def platform_detail(request,uuid):
    platform = get_object_or_404(Platform, uuid=uuid)
    # platform = Platform.objects.get(pk=uuid)
    allow_list = platform.iptables_set.all()
    return render(request,'business/platform_detail.html',locals())

@permission_required('business.Can_add_business', login_url='/auth_error/')
def platform_edit(request,uuid):
    platform = get_object_or_404(Platform, uuid=uuid)
    pf = PlatfForm(instance=platform)

    server_all = Server.objects.all()
    front_station_host = platform.front_station.all()
    front_proxy_host = platform.front_proxy.all()
    front_image_host = platform.front_image_site.all()
    front_download_host = platform.front_download_site.all()
    front_active_host = platform.front_active_site.all()
    front_active_cache_host = platform.front_active_cache.all()

    backend_station_host = platform.backend_station.all()
    backend_proxy_host = platform.backend_proxy.all()
    backend_image_host = platform.backend_image_site.all()
    backend_active_host = platform.backend_active_site.all()

    front_station_all = [p for p in server_all if p not in front_station_host]
    front_proxy_all  = [p for p in server_all if p not in front_proxy_host]
    front_image_all  = [p for p in server_all if p not in front_image_host]
    front_download_all  = [p for p in server_all if p not in front_download_host]
    front_active_all  = [p for p in server_all if p not in front_active_host]
    front_active_cache_all  = [p for p in server_all if p not in front_active_cache_host]

    backend_station_all  = [p for p in server_all if p not in backend_station_host]
    backend_proxy_all  = [p for p in server_all if p not in backend_proxy_host]
    backend_image_all  = [p for p in server_all if p not in backend_image_host]
    backend_active_all  = [p for p in server_all if p not in backend_active_host]

    allow_list = platform.iptables_set.all()
    if request.method == 'POST':
        pf = PlatfForm(request.POST,instance=platform)
        if pf.is_valid():
            p_data = pf.save()
            return HttpResponseRedirect('/allow/welcome/')
    return render(request,'business/platform_edit.html',locals())

##域名增删查改
@permission_required('business.Can_add_business', login_url='/auth_error/')
def domain_list(request):
    domain_data = DomainName.objects.all()
    return render(request,'business/domain_list.html',locals())

@permission_required('business.Can_add_business', login_url='/auth_error/')
def domain_add(request):
    df = DomainNameForm()
    if request.method == 'POST':
        df = DomainNameForm(request.POST)
        if df.is_valid():
            df_data = df.save()
            return HttpResponseRedirect('/allow/welcome/')
    return render(request,'business/domain_add.html',locals())

@permission_required('business.Can_add_business', login_url='/auth_error/')
def domain_edit(request,uuid):
    domainname = get_object_or_404(DomainName, uuid=uuid)
    df = DomainNameForm(instance=domainname)
    if request.method == 'POST':
        df = DomainNameForm(request.POST,instance=domainname)
        if df.is_valid():
            df_data = df.save()
            return HttpResponseRedirect('/allow/welcome/')
    return render(request,'business/domain_edit.html',locals())

@permission_required('business.Can_add_business', login_url='/auth_error/')
def domain_delete(request,uuid):
    domainname = get_object_or_404(DomainName, uuid=uuid)
    domainname.delete()
    return render(request,'business/domain_list.html',locals())

@permission_required('business.Can_add_domainname', login_url='/auth_error/')
def domain_detail(request,uuid):
    domain_data = get_object_or_404(DomainName, uuid=uuid)
    return render(request,'business/domain_detail.html',locals())


@permission_required('business.Can_add_domainname', login_url='/auth_error/')
def domain_add_batch(request):
    """批量添加域名"""
    if request.method == 'POST':
        multi_domainname = request.POST.get('batch').split('\n')
        for domainname in multi_domainname:
            if domainname == '':
                break
            name,use,business = domainname.split('@')
            business = get_object_or_404(Business,name=business)
            if business:
                if use == u'前端域名':
                    use = '0'
                elif use == u'接口域名':
                    use = '1'
                elif use == u'后台域名':
                    use = '2'
                else:
                    emg = u'用途格式错误(前端域名|接口域名|后台域名)！'
                    return render(request,'business/domain_add_batch.html')
            else:
                emg = u'业务名称格式错误(新菲律宾|老菲律宾)！'
                return render(request,'business/domain_add_batch.html')

            domain_data = DomainName(name=name,use=use,business=business,state='0',status=True)
            domain_data.save()
        smg = u'批量添加成功.'
        return render(request,'business/domain_add_batch.html',locals())

    return render(request,'business/domain_add_batch.html',locals())




##故障增删查改
@permission_required('business.Can_add_business', login_url='/auth_error/')
def bugs_list(request):
    bugs_data = Bugs.objects.all()
    return render(request,'business/bugs_list.html',locals())

