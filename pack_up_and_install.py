#!usr/bin/python
# -*- coding: utf-8 -*-
#
# file_name: pack_up_and_install.py
# description: 
# author: libo
# Histort:
# 	first created: 2015/11/27

__author__ = 'libo'

import os
import subprocess

from lib import PyLogger

PACKEAGE_NAME = "PyLogger"

curr_dir = os.path.split(os.path.realpath(__file__))[0]
version = PyLogger.__version__
package_name = "%s-%s-py2.7.egg"%(PACKEAGE_NAME, version)
# setup


setup = subprocess.Popen("python %s bdist_egg"%os.path.join(curr_dir, "setup.py"))
setup.wait()
install = subprocess.Popen("easy_install %s"%os.path.join(curr_dir, "dist", package_name))
install.wait()

