from fabric.api import put, run, settings, task
from fabric.contrib.files import exists, sed
from StringIO import StringIO

from . import apt

@task
def ensure(server=None):
    with settings(user='root'):
        apt.add_repository('ppa:certbot/certbot')
        apt.ensure('certbot')
        if exists('/etc/letsencrypt/renewal-hooks/deploy') and server is not None:
            hook = StringIO()
            hook.name = server
            hook.write('#!/bin/sh')
            hook.write('systemctl reload %s' % server)
            put(hook, '/etc/letsencrypt/renewal-hooks/deploy/%s' % server)

@task
def request(webroot, domains, email=None):
    if email is None:
        email = 'hostmaster@' + '.'.join(domains[0].split('.')[-2:])
    with settings(user='root'):
        cmd = [
            'certbot',
            'certonly',
            '--email', email,
            '--agree-tos',
            '--no-eff-email',
            '--webroot',
            '--webroot-path', webroot,
        ]
        for domain in domains:
            cmd.extend(['-d', domain])
        run(' '.join(cmd))
