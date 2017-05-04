from fabric.api import run, settings, task
from fabric.contrib.files import sed

from . import apt

@task
def ensure():
    with settings(user='root'):
        apt.add_repository('ppa:certbot/certbot')
        apt.ensure('certbot')
        sed('/etc/cron.d/certbot',
            'certbot -q renew',
            'certbot -q renew \\&\\& service nginx reload', backup='')

@task
def request(webroot, domain, email=None):
    if email is None:
        email = 'hostmaster@' + '.'.join(domain.split('.')[-2:])
    with settings(user='root'):
        cmd = [
            'certbot',
            'certonly',
            '--email', email,
            '--agree-tos',
            '--no-eff-email',
            '--webroot',
            '--webroot-path', webroot,
            '-d', domain
        ]
        run(' '.join(cmd))
