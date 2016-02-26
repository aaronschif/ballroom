from pathlib import Path
import hashlib
import os
import itertools
import shutil

import sass
import cairosvg
from PIL import Image
from doit.tools import create_folder


def _minify_svg(task):
    (filename,) = task.file_dep
    (target,) = task.targets

    with open(target, 'wb') as o:
        o.write(
            cairosvg.svg2svg(url=filename)
            )

def _hash_asset(task):
    (filename,) = task.file_dep

    with open(filename, 'rb') as f:
        m = hashlib.md5()
        m.update(f.read())
        digest = m.hexdigest()[:10]

    file_path = Path(filename)
    parent, name = str(file_path.parent), str(file_path.name)
    a, b = name.split('.', 1)

    link_filename = filename
    new_filename = '{}/{}.{}.{}'.format(parent, a, digest, b)
    old_filename = str(Path(link_filename).resolve())

    shutil.move(old_filename, new_filename)
    if os.path.exists(link_filename):
        os.remove(link_filename)
    os.symlink(Path(new_filename).name, link_filename)



def _convert_svg_png(task):
    (filename,) = task.file_dep
    (target,) = task.targets

    with open(target, 'wb') as o, open(filename) as i:
        o.write(
            cairosvg.svg2png(url=filename)
            )

def _convert_png_ico(task):
    (filename,) = task.file_dep
    (target,) = task.targets
    im = Image.open(filename)
    im.thumbnail((16, 16))
    im.save(target, 'GIF')

def _compile_sass(task):
    (filename,) = task.file_dep
    (target,) = task.targets

    with open(target, 'w') as f, open(filename) as i:
        f.write(
            sass.compile(string=i.read(), indented=True)
            )


def task_sass_files():
    OUTPUT = 'output/static/'

    yield {
        'name': None,
        'actions': [create_folder(OUTPUT)]
    }

    yield {
        'name': 'sass',
        'actions': [_compile_sass],
        'file_dep': ['ballroom_theme/static/css/main.sass'],
        'targets': [OUTPUT+'main.css'],
    }

def task_image_files():
    OUTPUT = 'output/static/'

    yield {
        'name': None,
        'actions': [create_folder(OUTPUT)]
    }

    yield {
        'name': 'svg',
        'actions': [_minify_svg],
        'file_dep': ['ballroom_theme/static/img/dancers.svg'],
        'targets': [OUTPUT+'dancers.min.svg'],
    }

    yield {
        'name': 'png',
        'actions': [_convert_svg_png],
        'file_dep': ['ballroom_theme/static/img/dancers.svg'],
        'targets': [OUTPUT+'dancers.png'],
    }

    yield {
        'name': 'ico',
        'actions': [_convert_png_ico],
        'file_dep': ['ballroom_theme/static/img/dancers.png'],
        'targets': [OUTPUT+'dancers.gif'],

    }

def task_hash_assets():
    for f in itertools.chain(task_image_files(), task_sass_files()):
        for i in f.get('targets', []):
            yield {
                'name': i,
                'actions': [_hash_asset],
                'file_dep': [i],
            }

# def task_pelican():
#     yield {
#         'name': 'pelican',
#         'actions': ['pelican content -s config/local.py -o output'],
#         'task_dep': ['image_files', 'sass_files'],
#     }
