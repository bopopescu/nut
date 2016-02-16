#!/usr/bin/env python

import os
import ConfigParser

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.project import rsync_project


Config = ConfigParser.ConfigParser()
Config.read('fetch_conf.ini')
root_dir = os.path.join(os.getcwd(), '..')
env.hosts = ['114.113.154.48']
env.user = Config.get('global', 'user')
env.local_root = os.path.join(root_dir, Config.get('local', 'project_dir'))
env.project_root = Config.get('server', 'project_dir')


@parallel
def upload_code():
    rsync_project(
        remote_dir=env.project_root,
        local_dir=env.local_root,
        delete=True,
        extra_opts="--password-file='guoku.pass' --exclude='/images' "
    )


def upload():
    execute(upload_code)
