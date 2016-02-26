from pathlib import Path
import hashlib
import os
import itertools
import shutil
from docutils.core import publish_parts

import sass
import cairosvg
from PIL import Image
from jinja2 import Environment, meta, FileSystemLoader, environmentfilter, Markup
from doit.tools import create_folder


TEMPLATES_DIR = 'ballroom_theme/templates/'
OUTPUT_DIR = 'output/'
OUTPUT_STATIC = 'output/static/'

def _jinja_rst(f):
    html = publish_parts(source=str(f), writer_name='html')['body']
    return Markup(html)

def _jinja_resolve_asset(f):
    path = Path(OUTPUT_DIR+f).resolve()
    output = Path(OUTPUT_DIR).resolve()
    return str(path.relative_to(output))

env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR)
)
env.filters['static'] = _jinja_resolve_asset
env.filters['load_rst'] = _jinja_rst

def _minify_svg(task):
    (filename,) = task.file_dep
    (target,) = task.targets

    with open(target, 'wb') as o:
        o.write(
            cairosvg.svg2svg(url=filename)
            )

def _cp(task):
    (filename,) = task.file_dep
    (target,) = task.targets

    shutil.copy(filename, target)

def _compile_jinja(filename, target):
    # (filename,) = task.file_dep
    # # (target,) = task.targets
    # target = f

    t = env.get_template(filename)

    with open(target, 'w') as f:
        f.write(t.render())

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
        'targets': [OUTPUT+'dancers.svg'],
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

    yield {
        'name': 'facebook',
        'actions': [_cp],
        'file_dep': ['ballroom_theme/static/img/facebook.png'],
        'targets': [OUTPUT+'facebook.png'],

    }

    yield {
        'name': 'youtube',
        'actions': [_cp],
        'file_dep': ['ballroom_theme/static/img/youtube.png'],
        'targets': [OUTPUT+'youtube.png'],

    }

    yield {
        'name': 'email',
        'actions': [_cp],
        'file_dep': ['ballroom_theme/static/img/email.png'],
        'targets': [OUTPUT+'email.png'],

    }


def task_hash_assets():
    for f in itertools.chain(task_image_files(), task_sass_files()):
        for i in f.get('targets', []):
            yield {
                'name': i,
                'actions': [_hash_asset],
                'file_dep': [i],
            }

def task_html_files():
    OUTPUT = 'output/'
    deps = [TEMPLATES_DIR+f for f in env.list_templates()]
    yield {
        'name': None,
        'actions': [create_folder(OUTPUT)],
        'task_dep': ['hash_assets'],
    }

    yield {
        'name': 'index',
        'actions': [(_compile_jinja, ['index.html', OUTPUT+'index.html'])],
        'file_dep': deps,
    }

    yield {
        'name': 'faq',
        'actions': [(_compile_jinja, ['faq.html', OUTPUT+'faq.html'])],
        'file_dep': deps
    }

# def task_pelican():
#     yield {
#         'name': 'pelican',
#         'actions': ['pelican content -s config/local.py -o output'],
#         'task_dep': ['image_files', 'sass_files'],
#     }
