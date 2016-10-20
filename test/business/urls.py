#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from business import views


urlpatterns = [
    url(r'^business_list/$', views.business_list, name="business_list"),
    url(r'^bugs_list/$', views.bugs_list, name="bugs_list"),




]