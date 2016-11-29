#!/usr/bin/env python
# coding:utf-8


from __future__ import absolute_import, unicode_literals
from celery import shared_task,current_task
from api.ansible_api import ansiblex_deploy


@shared_task()
def deploy_use_ansible(x):
    task_path = x
    current_task.update_state(state="PROGRESS")
    ansiblex_deploy(vars1=task_path)


    return random.random()
