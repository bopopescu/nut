#!/usr/bin/env python

import ConfigParser
import os

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.project import rsync_project

Config = ConfigParser.ConfigParser()
Config.read('config.ini')

root_dir = os.path.join(os.getcwd(), '..')

env.hosts = ['114.113.154.48']

env.user = Config.get('global', 'user')
env.key = os.path.expanduser(Config.get('global', 'key'))

env.local_root = os.path.join(root_dir, Config.get('local', 'project_dir'))
env.project_root = Config.get('server', 'project_dir')


@parallel
def upload_code():
    ssh_opts = '-i {}'.format(env.key)
    rsync_project(
        remote_dir=env.project_root,
        local_dir=env.local_root,
        delete=True,
        ssh_opts=ssh_opts
    )


def upload():
    execute(upload_code)
