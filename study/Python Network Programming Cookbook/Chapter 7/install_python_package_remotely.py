# -*- coding: utf-8 -*-

# 在远程主机中安装 Python 包

# ln -s install_python_package_remotely.py fabfile.py

from getpass import getpass
from fabric.api import settings, run, env, prompt

def remote_server():
    env.hosts = ['10.10.9.144']
    env.user = prompt('Enter user name: ')
    env.password = getpass('Enter password: ')

def install_package():
    run("pip install yolk")
