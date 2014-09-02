from fabric.api import *
import fabric.contrib.project as project
import os

env.build_path = 'output'
env.content_path = 'content'

env.production_serve = '/usr/local/data/www/ballroom'
env.alpha_serve = '/usr/local/data/www/ballroom/_alpha'

production = 'aaronschif@unix.ksu.edu:22'
dest_path = '/usr/local/data/www/ballroom'

def clean():
    if os.path.isdir(env.build_path):
        local('rm -rf {build_path}'.format(**env))
        local('mkdir {build_path}'.format(**env))

def build(settings='local'):
    local('pelican {content_path} -s config/{settings}.py -o output'.format(settings=settings, **env))

def rebuild():
    clean()
    build()

def regenerate(settings='local'):
    local('pelican {content_path} -r -s config/{settings}.py -o output'.format(settings=settings, **env))

def serve():
    local('cd {build_path} && python -m SimpleHTTPServer'.format(**env))

def reserve():
    build()
    serve()

@hosts(production)
def publish(role='alpha'):
    clean()
    build(role)
    project.rsync_project(
        remote_dir=getattr(env, role+'_serve'),
        local_dir=env.build_path.rstrip('/') + '/',
        extra_opts='--omit-dir-times --no-perms',
        exclude='_alpha',
        delete=True
    )
    
    # put(
    #     env.build_path,
    #     dest_path
    # )

