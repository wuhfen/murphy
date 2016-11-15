#!/usr/bin/env python
# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Iptables, oldsite_line 
from .forms import IptablesForm
# Create your views here.
from api.ansible_api import ansiblex
import datetime
import json
import urllib2
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from django.core.urlresolvers import reverse

def error(request):
    return render(request,'allow_list/error.html')

def welcome(request):
    if 'user_name' in request.GET:
        return HttpResponse('Welcome!~'+request.GET['user_name'])
    else:
        return render(request,'allow_list/welcome.html',locals())

# def ansible_action(vars1,vars2,vars3="all_site",vars4="HTTP"):
#     ip = vars1                 #要插入或删除的ip
#     playbook_path = vars2       #执行的playbook名称
#     host_group = vars3          #指定要执行的组或主机名
#     comment = vars4             #防火墙规则上的备注

#     variable_manager = VariableManager()
#     loader = DataLoader()
#     inventory = Inventory(loader=loader, variable_manager=variable_manager,  host_list='/etc/ansible/hosts')
#     Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
#     options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=30, remote_user='root', private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root', verbosity=None, check=False)
 
#     variable_manager.extra_vars = {'ip': ip, 'host_group': host_group,'comment': comment }
#     passwords = {}

#     pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)
#     results = pbex.run()
#     return results


@permission_required('Allow_list.add_iptables', login_url='/allow/error/')
def iptables(request):
    ff = IptablesForm()
    fo_errors = []
    view_rules = Iptables.objects.filter(i_comment__contains="WEB_PORT_")
    if 'okk' in request.POST:
        ff = IptablesForm(request.POST)
        if ff.is_valid():
            ip = str(ff.cleaned_data.get('ipaddr'))
            comment = ff.cleaned_data.get('comment')
            remark = ff.cleaned_data.get('remark')
            if remark == u"only_new":
                host_group = u"新平台"
                chain = "INPUT"
            else:
                host_group = u"老平台"
                chain = "FORWARD"
            # else:
            #     host_group = u"全平台"
            #     chain = "INPUT"
            ip_api = "http://freeapi.ipip.net/%s" % ip
            req = urllib2.Request(ip_api)
            rel = urllib2.urlopen(req).read()
            result = rel.strip('[]').replace('\"','').split(',')
            # if ("中国" not in result) and ("香港" not in result):
            #     fo_errors.append("你输入的IP是:%s,IP属于:%s,添加状态：失败" % (ip,rel))
            if not fo_errors:
                comment = u"WEB_PORT_%s" % comment
                user = request.user
                i = Iptables(i_comment=comment,i_chain=chain,i_source_ip=ip,i_user=user,i_remark=remark,i_tag=host_group)
                i.save()
                task = "/etc/ansible/insertip.yml"
                ansiblex(task,ip,remark,comment)
                return HttpResponseRedirect('/allow/welcome/')
    return render(request,'allow_list/iptables.html',locals())



    # view_rules = Iptables.objects.filter(i_comment__contains="WEB_PORT_")
    # fo_errors = []
    # if 'okk' in request.POST:
    #     ff = IptablesForm(request.POST)
    #     ip = str(request.POST['ipaddr'])
    #     comment = request.POST['comment']
    #     ip_api = "http://freeapi.ipip.net/%s" % ip
    #     if 'choice' in request.POST:
    #         choice = request.POST['choice']
    #         if choice == u"only_new":
    #             host_group = u"新源站"
    #         else:
    #             host_group = u"老源站"
    #         if ff.is_valid():
    #             host_ip = '10.10.239.145'
    #             comment = u"WEB_PORT_%s" % comment
    #             method = "I"
    #             chain = "INPUT"
    #             position = "3"
    #             source_ip = ip
    #             destination_ip = "0.0.0.0"
    #             protocol = "tcp"
    #             port_method = "--dport"
    #             ports = '80,443'
    #             states = "NEW,ESTABLISHED"
    #             target = "ACCEPT"
    #             date_time = datetime.datetime.now()
    #             user = request.user
    #             req = urllib2.Request(ip_api)
    #             rel = urllib2.urlopen(req).read()
    #             result = rel.strip('[]').replace('\"','').split(',')
    #             if ("中国" not in result) and ("香港" not in result):
    #                 fo_errors.append("你输入的IP是:%s,IP属于:%s,添加状态：失败" % (ip,rel))
    #             if not fo_errors:
    #                 i = Iptables(host_ip=host_ip,i_comment=comment, i_table='filter',i_method=method,i_chain=chain,i_position=position,i_source_ip=source_ip,i_destination_ip=destination_ip,i_protocol=protocol,i_port_method=port_method,i_ports=ports,i_states=states,i_target=target,i_date_time=date_time,i_user=user,i_remark=host_group)
    #                 i.save()
    #                 task = "/etc/ansible/insertip.yml"
    #                 ansiblex(task,ip,choice,comment)
    #                 ff = IptablesForm()
    #                 return HttpResponseRedirect('/allow/welcome/')
    #     else:
    #         fo_errors.append("你没有选择站点！")
    # else:
    #     ff = IptablesForm()
    #return render(request,'allow_list/iptables.html',locals())


@permission_required('Allow_list.change_iptables', login_url='/allow/error/')
def iptables_delete(request):
    ff = IptablesForm()
    search_rules = Iptables.objects.filter(i_comment__contains="WEB_PORT_")
    if request.method == 'POST':
        if "delete" in request.POST:
            ruls_id = str(request.POST['delete'])
            delete_ruls = Iptables.objects.get(id=ruls_id)
            ipaddr = delete_ruls.i_source_ip
            remark = delete_ruls.i_remark
            comm = delete_ruls.i_comment
            delete_ruls.delete()
            task = "/etc/ansible/deleteip.yml"
            ansiblex(task,str(ipaddr),remark,comm)
            infos = "IP: %s 已经成功解除绑定" % str(ipaddr)
            #return HttpResponse(choice)
            return HttpResponseRedirect('/allow/welcome/')
        elif "searchcomment" in request.POST:
            ff = IptablesForm(request.POST)
            comment = request.POST.get('comment')
            search_rules = Iptables.objects.filter(i_comment__contains="%s"% comment)
            return render(request,"allow_list/iptables_delete.html",locals())
        else:
            ip = request.POST.get('searchip')
            search_rules = Iptables.objects.filter(i_source_ip__contains="%s"% ip)
            return render(request,"allow_list/iptables_delete.html",locals())

    return render(request,"allow_list/iptables_delete.html",locals())


# def ansiblex(vars1="1",vars2="2",vars3="3",vars4="4",vars5="5",vars6="6"):
#     one_var=vars1
#     two_var=vars2
#     three_var=vars3
#     four_var=vars4
#     five_var=vars5
#     six_var=vars6

#     variable_manager = VariableManager()
#     loader = DataLoader()
#     inventory = Inventory(loader=loader, variable_manager=variable_manager,  host_list='/etc/ansible/hosts')
#     Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
#     options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=30, remote_user='root', private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root', verbosity=None, check=False)
 
#     variable_manager.extra_vars = {'two_var': two_var, 'three_var': three_var,'four_var': four_var, 'five_var': five_var, 'six_var': six_var}
#     passwords = {}

#     pbex = PlaybookExecutor(playbooks=[one_var], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)
#     results = pbex.run()
#     return results



@permission_required('Allow_list.change_oldsite_line', login_url='/allow/error/')
def linechange(request):
    line_errors = []
    if "change" in request.POST:
        if "choiceline" not in request.POST:
            line_errors.append("你没有选择需要切换的线路！")
        elif "choiceagent" not in request.POST:
            line_errors.append("你没有选择客户！")
        else:
            choiceagent = request.POST['choiceagent']
            choiceline = request.POST['choiceline']
            oldsite_line.objects.filter(agent_name__contains=choiceagent).update(status=False)
            if choiceline == u"line_one":
                oldsite_line.objects.filter(agent_name__contains=choiceagent).filter(number=1).update(status=True)
            elif choiceline == u"line_two":
                oldsite_line.objects.filter(agent_name__contains=choiceagent).filter(number=2).update(status=True)
            elif choiceline == u"line_three":
                oldsite_line.objects.filter(agent_name__contains=choiceagent).filter(number=3).update(status=True)
            
            task = "/etc/ansible/changeline.yml"
            ansiblex(task,choiceagent,choiceline)

            return HttpResponseRedirect('/allow/welcome/')
        return render(request,"allow_list/linechange.html",locals())
    elif "search" in request.POST:
        if "choiceagent" not in request.POST:
            line_errors.append("你没有选择客户！")
        else:
            choiceagent = request.POST['choiceagent']
            search_lines = oldsite_line.objects.filter(agent_name__contains=choiceagent)
        return render(request,"allow_list/linechange.html",locals())
    else:
        return render(request,"allow_list/linechange.html",locals())