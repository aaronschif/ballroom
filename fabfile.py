from fabric.api import *
import fabric.contrib.project as project
import os

env.deploy_path = 'output'
env.content_path = 'content'

production = 'aaronschif@unix.ksu.edu:22'
dest_path = '/usr/local/data/www/ballroom'

def clean():
    if os.path.isdir(env.deploy_path):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def build(settings='local'):
    local('pelican {content_path} -s config/{settings}.py -o output'.format(settings=settings, **env))

def rebuild():
    clean()
    build()

def regenerate():
    local('pelican -r -s config/local.py')

def serve():
    local('cd {deploy_path} && python -m SimpleHTTPServer'.format(**env))

def reserve():
    build()
    serve()

@hosts(production)
def publish():
    clean()
    build('production')
    project.rsync_project(
        remote_dir=dest_path,
        local_dir=env.deploy_path.rstrip('/') + '/',
        extra_opts='--omit-dir-times --no-perms',
        delete=True
    )
    # put(
    #     env.deploy_path,
    #     dest_path
    # )

