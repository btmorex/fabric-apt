from fabric.api import hide, put, run, settings, task
from StringIO import StringIO

from . import apt

@task
def ensure():
    with settings(user='root'):
        run('wget --quiet https://www.postgresql.org/media/keys/ACCC4CF8.asc')
        run('apt-key add ACCC4CF8.asc')
        run('rm ACCC4CF8.asc')
        with hide('commands'):
            codename = run('lsb_release --codename --short')
        sources = StringIO()
        sources.name = 'pgdg.list'
        sources.write('deb http://apt.postgresql.org/pub/repos/apt/ {}-pgdg main\n'.format(codename))
        put(sources, '/etc/apt/sources.list.d/pgdg.list')
        apt.update()
        apt.ensure('postgresql')

@task
def delete_user(user):
    with settings(user='root'):
        run('su --login --command "dropuser --if-exists {}" postgres'.format(user))

@task
def create_user(user):
    delete_user(user)
    with settings(user='root'):
        run('su --login --command "createuser {}" postgres'.format(user))

@task
def delete_db(db):
    with settings(user='root'):
        run('su --login --command "dropdb --if-exists {}" postgres'.format(db))
@task
def create_db(db, user):
    delete_db(db)
    with settings(user='root'):
        run('su --login --command "createdb --owner={} {}" postgres'.format(user, db))
