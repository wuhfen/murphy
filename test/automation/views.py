#!/usr/bin/env python
# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404

from automation.models import Tools, Confile, deploy
from automation.forms import ToolsForm, ConfileFrom, DeployForm
# Create your views here.
from api.git_api import Repo
import os.path

@permission_required('automation.Can_add_Tools', login_url='/auth_error/')
def tools_add(request):
    tf = ToolsForm()
    tf_errors = []
    data = Tools.objects.all()
    title = request.POST.get('title', '')
    url = request.POST.get('address', '')
    if Tools.objects.filter(title=title):
        tf_errors.append(u"所填标题已存在")
    if Tools.objects.filter(address=url):
        tf_errors.append(u"所填地址已存在")

    if request.method == 'POST':
        tf = ToolsForm(request.POST)
        if tf.is_valid():
            if not tf_errors:
                tf_data = tf.save()
            return HttpResponseRedirect('/success/')

    # return HttpResponse("success")
    return render(request,'automation/tools_add.html',locals())

@permission_required('automation.Can_add_Tools', login_url='/auth_error/')
def tools_list(request):
    data = Tools.objects.all()
    return render(request,'automation/tools_list.html',locals())

@permission_required('automation.Can_add_Tools', login_url='/auth_error/')
def tools_edit(request,uuid):
    data = Tools.objects.get(pk=uuid)
    tf = ToolsForm(instance=data)
    if request.method == 'POST':
        tf = ToolsForm(request.POST,instance=data)
        if tf.is_valid():
            tf_data = tf.save()
            return HttpResponseRedirect('/success/')

    return render(request,'automation/tools_edit.html',locals())

@permission_required('automation.Can_delete_Tools', login_url='/auth_error/')
def tools_delete(request,uuid):
    data = get_object_or_404(Tools,uuid=uuid)
    if data:
        data.delete()
        return HttpResponse("success")
    
    return render(request,'automation/tools_list.html',locals())

@permission_required('automation.Can_add_Confile', login_url='/auth_error/')
def conf_add(request):
    cf = ConfileFrom()
    cf_errors = []
    title = request.POST.get('name', '')
    path = request.POST.get('localhost_dir', '')

    if Tools.objects.filter(name=title):
        cf_errors.append(u"所填标题已存在")

    if request.method == 'POST':
        cf = ConfileFrom(request.POST)
        if cf.is_valid():
            if not cf_errors:
                cf_data = cf.save()
                if os.path.isdir(path):
                    pass
                else:
                    os.makedirs(path)
            return HttpResponseRedirect('/success/')

    # return HttpResponse("success")
    return render(request,'automation/conf_add.html',locals())

@permission_required('automation.Can_add_Confile', login_url='/auth_error/')
def conf_list(request):
    data = Confile.objects.all()
    return render(request,'automation/conf_list.html',locals())

@permission_required('automation.Can_delete_Confile', login_url='/auth_error/')
def conf_delete(request,uuid):
    data = get_object_or_404(Tools,uuid=uuid)
    if data:
        data.delete()
        return HttpResponse("SUCCESS!")
    return render(request,'automation/deploy_business.html',locals())

@permission_required('automation.Can_change_Confile', login_url='/auth_error/')
def conf_edit(request,uuid):
    data = Confile.objects.get(pk=uuid)
    cf = ConfileFrom(instance=data)
    if request.method == 'POST':
        cf = ConfileFrom(request.POST,instance=data)
        if cf.is_valid():
            cf_data = cf.save()
            return HttpResponseRedirect('/success/')

    return render(request,'automation/conf_edit.html',locals())

@permission_required('automation.Can_add_Confile', login_url='/auth_error/')
def conf_detail(request,uuid):
    data = Confile.objects.get(pk=uuid)
    if data:
        cf = ConfileFrom(instance=data)
    return render(request,'automation/conf_detail.html',locals())

@permission_required('automation.Can_add_Confile', login_url='/auth_error/')
def conf_copy(request,uuid):
    data = Confile.objects.get(pk=uuid)
    data.save()
    name = data.name + "- copy"
    if data:
        new_data = data
        new_data.pk = None
        new_data.name = name
        new_data.save()
    return HttpResponse("copy model success!")


@permission_required('automation.Can_add_Confile', login_url='/auth_error/')
def conf_check(request,uuid):
    data = Confile.objects.get(pk=uuid)
    git_addr = data.tool.address
    path = data.localhost_dir

    repo = Repo(path)
    bb = repo.git_all_branch()




    return HttpResponse(bb)




@permission_required('automation.Can_add_Confile', login_url='/auth_error/')
def deploy_business(request):
    data = Confile.objects.all()

    return render(request,'automation/deploy_business.html',locals())

@permission_required('automation.Can_add_Confile', login_url='/auth_error/')
def deploy_add(request,uuid):
    data = Confile.objects.get(pk=uuid)
    git_addr = data.tool.address
    path = data.localhost_dir
    repo = Repo(path)
    branch = repo.git_branch


    df = DeployForm()
    df_errors = []

    return render(request,'automation/deploy_add.html',locals())