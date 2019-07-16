#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: sunjun
# Mail: 50191646@qq.com
# Created Time:  <datetime: 2019-07-03 22:12:35>  
#############################################
  
from setuptools import setup, find_packages

setup(
    name = "tensor-tracer",
    version = "0.1",
    keywords = ("pip", "tracer","tensor"),
    description = "deeplearning tracer",
    long_description = "trace deeplearning python script",
    license = "MIT Licence",

    url = "",
    author = "SunJun",
    author_email = "50191646@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy","torch"],
    scripts = ['bin/ttracer', "bin/ttracer_invoker"]
)
