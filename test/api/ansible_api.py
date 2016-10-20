#!/usr/bin/env python
# coding:utf-8

import datetime
import json
import urllib2
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from django.core.urlresolvers import reverse

## 引入ansibleAPI，编写调用API的函数
def ansiblex(vars1="1",vars2="2",vars3="3",vars4="4",vars5="5",vars6="6"):
    one_var=vars1
    two_var=vars2
    three_var=vars3
    four_var=vars4
    five_var=vars5
    six_var=vars6

    variable_manager = VariableManager()
    loader = DataLoader()
    inventory = Inventory(loader=loader, variable_manager=variable_manager,  host_list='/etc/ansible/hosts')
    Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
    options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=30, remote_user='root', private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root', verbosity=None, check=False)
 
    variable_manager.extra_vars = {'two_var': two_var, 'three_var': three_var,'four_var': four_var, 'five_var': five_var, 'six_var': six_var}
    passwords = {}

    pbex = PlaybookExecutor(playbooks=[one_var], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)
    results = pbex.run()
    return results