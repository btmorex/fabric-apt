from fabric.api import hide, put, run, settings, task
from StringIO import StringIO

from . import apt

@task
def ensure():
    with settings(user='root'):
        run('wget --quiet https://deb.nodesource.com/gpgkey/nodesource.gpg.key')
        run('apt-key add nodesource.gpg.key')
        run('rm nodesource.gpg.key')
        with hide('commands'):
            codename = run('lsb_release --codename --short')
        sources = StringIO()
        sources.name = 'nodesource.list'
        sources.write('deb https://deb.nodesource.com/node_8.x {} main\n'.format(codename))
        put(sources, '/etc/apt/sources.list.d/nodesource.list')
        run('wget --quiet https://dl.yarnpkg.com/debian/pubkey.gpg')
        run('apt-key add pubkey.gpg')
        run('rm pubkey.gpg')
        sources = StringIO()
        sources.name = 'yarn.list'
        sources.write('deb https://dl.yarnpkg.com/debian/ stable main\n')
        put(sources, '/etc/apt/sources.list.d/yarn.list')
        apt.update()
        apt.ensure('apt-transport-https')
        apt.ensure('nodejs')
        apt.ensure('yarn')
