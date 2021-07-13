#!/usr/bin/env python
# encoding: utf-8
"""
@author: liubowen
@contact: 15178940382@163.com
@site: http://www.liubowen.icu/
@file: my_forms.py
@time: 2021/7/13 17:06
"""
from django import forms
from django.core.exceptions import ValidationError
from .views import StudentInformationModel


class EmpForm(forms.Form):
    name = forms.CharField
