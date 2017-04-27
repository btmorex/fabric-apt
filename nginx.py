from fabric.api import hide, put, run, settings, task
from StringIO import StringIO

from . import apt

@task
def ensure():
    with settings(user='root'):
        run('wget --quiet http://nginx.org/keys/nginx_signing.key')
        run('apt-key add nginx_signing.key')
        run('rm nginx_signing.key')
        with hide('commands'):
            codename = run('lsb_release --codename --short')
        sources = StringIO()
        sources.name = 'nginx.list'
        sources.write('deb http://nginx.org/packages/ubuntu/ {} nginx\n'.format(codename))
        put(sources, '/etc/apt/sources.list.d/nginx.list')
        apt.update()
        apt.ensure('nginx')
        run('nginx -t')
