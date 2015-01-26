#!/usr/bin/env python


import ConfigParser

from fabric.api import *
from fabric.context_managers import *

Config = ConfigParser.ConfigParser()
Config.read('config.ini')


env.hosts = ['114.113.154.47', '114.113.154.46' ]
env.user = Config.get('global', 'user')
env.key = Config.get('global', 'key')
env.password = 'jessie1@#'

script_dir = Config.get('server', 'script_dir')

def reload_gunicorn():
	with cd(script_dir):
		sudo('/bin/bash ./gunicorn reload')

def restart_celery():
    with cd(script_dir):
        sudo('/bin/bash ./celeryd restart')

def reload():
	# execute(sudo)
	execute(reload_gunicorn)
	execute(restart_celery)
