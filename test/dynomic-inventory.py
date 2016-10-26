#!/usr/bin/env python
# coding:utf-8

import urllib
import httplib2
import urllib2
import json
import argparse

def get_host_list():
    group = {'tag':"新平台"}
    urli = 'http://10.10.241.238/business/platform_api/?' + urllib.urlencode(group)
    req = urllib2.Request(urli)
    rel = urllib2.urlopen(req).read()
    return json.loads(rel)

def getList(inventory):
    '''get list hosts group'''
    print json.dumps(inventory)
 
 
def getVars(host,inventory):
    '''Get variables about a specific host'''
    print json.dumps(inventory['_meta']['hostvars'][host])


if __name__ == "__main__":
 
    parser = argparse.ArgumentParser()
    parser.add_argument('--list',action='store_true',dest='list',help='get all hosts list')
    parser.add_argument('--host',action='store',dest='host',help='get vars')
    args = parser.parse_args()

    if args.list:
        getList(get_host_list())

    if args.host:
        getVars(args.host,get_host_list())
