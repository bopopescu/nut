#!/bin/bash

find ../ -name '*.pyc' -exec rm {} \;
#FAB='/Users/edison7500/PycharmProjects/django15/bin/fab'
FAB=`which fab`

${FAB} -f upload_code.py upload
#${FAB} -f reload_server.py reload
#${FAB} -f upload_static.py deploy_static
