from fabric.api import run, settings, task

from .helper import run_as_root

def apt_get_cmd(cmd, *args):
    return ' '.join([
        'DEBIAN_FRONTEND=noninteractive',
        'apt-get',
        '--assume-yes',
        '--quiet',
        cmd,
    ] + list(args))

@task
def autoremove():
    run_as_root(apt_get_cmd('autoremove', '--purge'))

@task
def dist_upgrade():
    run_as_root(apt_get_cmd('dist-upgrade'))

@task
def ensure(pkg):
    run_as_root('dpkg --status %s 2&>1 >/dev/null || %s' % (pkg, apt_get_cmd('install', pkg)))

@task
def install(pkg):
    run_as_root(apt_get_cmd('install'), pkg)

@task
def purge(pkg):
    run_as_root(apt_get_cmd('purge'), pkg)

@task
def update():
    run_as_root(apt_get_cmd('update'))

@task
def upgrade():
    run_as_root(apt_get_cmd('upgrade'))

@task(default=True)
def full_upgrade():
    update()
    dist_upgrade()
    autoremove()
