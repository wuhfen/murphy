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
import shutil
import subprocess
import json
import time
from django.http import JsonResponse
from .tasks import deploy_use_ansible

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
    """实现添加发布的基本参数配置，但提交的时候会到指定的目录下面clone仓库"""
    cf = ConfileFrom()
    cf_errors = []
    name = request.POST.get('name', '')
    path = request.POST.get('localhost_dir', '')

    if Confile.objects.filter(name=name):
        cf_errors.append(u"所填标题已存在")
    if Confile.objects.filter(localhost_dir=path):
        cf_errors.append(u"所填仓库路径已存在")


    if request.method == 'POST':
        cf = ConfileFrom(request.POST)
        if cf.is_valid():
            if not cf_errors:
                cf_data = cf.save()            ##保存信息后先判断repo的clone路径存不存在，不存在则创建
                if os.path.isdir(path):
                    pass
                else:
                    os.makedirs(path)
                tool = cf_data.tool           ##创建clone的目录后将远程仓库clone下来
                url = tool.address
                repo = Repo(path)
                repo.git_clone(url,path)

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
    num = data.max_number
    repo = Repo(path)
    bb = repo.git_all_branch()         #获取所有的分支信息
    commit = repo.git_log(limit=num,template="--pretty=oneline")   #获取当前分支的log

    # return HttpResponse(commit)


    return render(request,'automation/conf_check.html',locals())




@permission_required('automation.Can_add_deploy', login_url='/auth_error/')
def deploy_business(request):
    data = Confile.objects.all()

    return render(request,'automation/deploy_business.html',locals())

@permission_required('automation.Can_add_deploy', login_url='/auth_error/')
def deploy_add(request,uuid):
    data = Confile.objects.get(pk=uuid)
    path = data.localhost_dir
    repo = Repo(path)
    pull = repo.git_pull(source="all")  ##在分支上先执行pull，更新到最新的仓库数据，相当于git pull --all
    branch = repo.git_all_branch()    ##拉取所有的分支信息，分支下面的commit_id是使用ajax获取
    tags = repo.git_tags()            ##拉取所有的tag信息

    df = DeployForm()
    df_errors = []

    if request.method == 'POST':
        if 'formtag' in request.POST:
            name = request.POST.get('tag_name','')
            tag = request.POST.get('tag','')
            memo = request.POST.get('tag_memo','')
            branches = "master"
            release = ''
            executive_user = request.user
            confile = data
            check_conf = "pass"
            status = "未发布"
            dtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            tag_data = deploy(dtime=dtime,name=name,branches=branches,release=release,executive_user=executive_user,
                confile=confile,check_conf=check_conf,status=status,tag=tag,memo=memo)
            tag_data.save()

            return HttpResponseRedirect('/success/')
        elif 'formbranch' in request.POST:
            dtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            name = request.POST.get('branch_name','')
            branches = request.POST.get('branches','')
            release = request.POST.get('release','')[0:8]
            executive_user = request.user
            confile = data
            check_conf = "pass"
            status = "未发布"
            tag = ''
            memo = request.POST.get('branch_memo','')
            branch_data = deploy(dtime=dtime,name=name,branches=branches,release=release,executive_user=executive_user,
                confile=confile,check_conf=check_conf,status=status,tag=tag,memo=memo)
            branch_data.save()
            return HttpResponseRedirect('/success/')

    return render(request,'automation/deploy_add.html',locals())



@permission_required('automation.Can_add_deploy', login_url='/auth_error/')
def deploy_branch_select(request):
    """这个函数定义如何获取仓库的commit_id，返回json数据给前端ajax"""
    branch = request.GET.get('branch','master')
    uuid = request.GET.get('uuid',0)
    data = Confile.objects.get(pk=uuid)
    path = data.localhost_dir
    num = data.max_number            ##这一项可以控制显示的commit_id的条数，但是要在git_log的limit参数中设置num，默认是10
    repo = Repo(path)
    change_branch = repo.git_checkout(branch)      ##切换到所选的分支上面
    pull = repo.git_pull(source="all")             ##在分支上先执行pull，更新到最新的仓库数据，相当于git pull --all
    commitid = repo.git_log(limit='10',template="--pretty=oneline")       ##在分支上面查看commit_id

    return JsonResponse(commitid,safe=False)

@permission_required('automation.Can_add_deploy', login_url='/auth_error/')
def deploy_list(request):
    data = deploy.objects.all()
    user = request.user
    if user.is_superuser:
        deploy_list = data
    else:
        deploy_list = data.filter(executive_user=user)
    # return HttpResponse(user.is_superuser)

    return render(request,'automation/deploy_list.html',locals())

@permission_required('automation.Can_delete_deploy', login_url='/auth_error/')
def deploy_online(request,uuid):
    data = get_object_or_404(deploy,pk=uuid)
    conf_data = data.confile
    branch = data.branches
    repo_path = conf_data.localhost_dir      ##这里需要做一个有没有repo clone的判断
    repo = Repo(repo_path)
    change_branch = repo.git_checkout("master")   ##切换到分支上面
    pull = repo.git_pull(source="all")          ##更新所有的分支
    ##step1 切换分支并切换到具体版本
    if data.release:
        change_version = repo.git_checkout(data.release)
    else:
        change_version = repo.git_checkout(data.git)
    ##step2 删除临时目录，因为下面cpoy代码的时候，目录不能存在，不然在这里应该要创建临时目录的
    path = '/tmp/coderepo/'
    if os.path.isdir(path):
        shutil.rmtree(path)      ##如果目录存在就删除，不存在就创建新的
        os.makedirs(path)
    else:
        os.makedirs(path)
    ##step3 代码拷贝到临时目录前需要执行的动作
    pre_deploy = conf_data.pre_deploy
    Lpre = [a for a in pre_deploy.split('\r\n') if a]
    for i in Lpre:
        res = subprocess.Popen(i,shell=True)
    ##step4 将代码拷贝到临时目录
    ignores = conf_data.exclude
    L = [a for a in ignores.split('/r/n') if a]
    src = repo_path
    dst = path
    shutil.copytree(src,dst,ignore=shutil.ignore_patterns(*L))
    ##step5 代码拷贝到临时目录后需要执行的一些动作
    post_deploy = conf_data.post_deploy
    Lpost = [a for a in post_deploy.split('\r\n') if a]
    for i in Lpost:
        res = subprocess.Popen(i,shell=True)
    ##step6 使用ansible将本地主机上的代码传送至远程服务器

    deploy_use_ansible.delay(task,ip,remark,comment)



    return render(request,'automation/deploy_online.html',locals())


