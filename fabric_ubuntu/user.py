from fabric.api import put, run, settings, task
from fabric.contrib.files import exists, uncomment

@task
def add(user, pub_id_rsa_file, force_bad_name=False):
    with settings(user='root'):
        if exists('/home/{}'.format(user)):
            run('deluser --remove-home --quiet {}'.format(user))
        adduser_flags = [
            '--disabled-password',
            '--gecos "{} user,,,"'.format(user),
            '--quiet',
        ]
        if force_bad_name:
            adduser_flags.append('--force-badname')
        run('adduser {} {}'.format(' '.join(adduser_flags), user))
        run('mkdir --mode=0700 /home/{}/.ssh'.format(user))
        put(pub_id_rsa_file, '/home/{}/.ssh/authorized_keys'.format(user))
        run('chown --recursive {0}: /home/{0}/.ssh'.format(user))
    with settings(user=user):
        uncomment('.profile', 'umask 022', backup='')
