from fabric.api import run, settings, task

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
    run(apt_get_cmd('autoremove', '--purge'))

@task
def dist_upgrade():
    run(apt_get_cmd('dist-upgrade'))

@task
def ensure(pkg):
    run('dpkg --status %s 2&>1 >/dev/null || %s' % (pkg, apt_get_cmd('install', pkg)))

@task
def install(pkg):
    run(apt_get_cmd('install'), pkg)

@task
def purge(pkg):
    run(apt_get_cmd('purge'), pkg)

@task
def update():
    run(apt_get_cmd('update'))

@task
def upgrade():
    run(apt_get_cmd('upgrade'))
