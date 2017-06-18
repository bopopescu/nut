#!/usr/bin/env python
import ConfigParser
import os

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.project import rsync_project

Config = ConfigParser.ConfigParser()
Config.read('config.ini')

root_dir = os.path.join(os.getcwd(), '..')

env.hosts = ['114.113.154.46']

env.user = Config.get('global', 'user')
env.key = os.path.expanduser(Config.get('global', 'key'))

# Where the static files get collected locally. Your STATIC_ROOT setting.
env.local_static_root = '/tmp/static/'

# Where the static files should go remotely
ver = local("git log | head -n 1 | awk '{print $2}'", capture=True)
print ver
static_path = '/data/www/core/static/v4/%s/' % ver
env.remote_static_root = static_path
print static_path


def deploy_static():
    ssh_opts = '-i {}'.format(env.key)
    with lcd('~/Workspace/guoku/nut/nut'):
        local('python manage.py collectstatic --noinput --settings="settings.stage"')
        local('sh ../deploy/clean_static.sh')
        local('sed  "s/v4\/.*/v4\/%s\/\'/" settings/production.py > settings/production.py.tmp' % ver)
        local("mv settings/production.py.tmp settings/production.py")
    rsync_project(
        remote_dir=env.remote_static_root,
        local_dir=env.local_static_root,
        ssh_opts=ssh_opts
    )
