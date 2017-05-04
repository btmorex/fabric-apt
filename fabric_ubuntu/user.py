from fabric.api import put, run, settings, task
from fabric.contrib.files import exists, uncomment

@task
def add(user, pub_id_rsa_file):
    with settings(user='root'):
        if exists('/home/{}'.format(user)):
            run('deluser --remove-home --quiet {}'.format(user))
        run('adduser --disabled-password --gecos "{0} user,,," --quiet {0}'.format(user))
        uncomment('.profile', 'umask 022', backup='')
        run('mkdir --mode=0700 /home/{}/.ssh'.format(user))
        put(pub_id_rsa_file, '/home/{}/.ssh/authorized_keys'.format(user))
        run('chown --recursive {0}: /home/{0}/.ssh'.format(user))
