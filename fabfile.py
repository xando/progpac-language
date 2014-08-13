from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm


def deploy():
    run('pip install https://github.com/xando/herbert/archive/master.zip --user --upgrade')
    with cd('webapps/herbert/progpac'):
        run("git pull")

    run('webapps/herbert/apache2/bin/restart')
