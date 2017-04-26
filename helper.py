from fabric.api import run, settings

def run_as_root(cmd):
    with settings(user='root'):
        run(cmd)
