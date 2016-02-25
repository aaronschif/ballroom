import sass
import cairosvg
from pathlib import Path
from PIL import Image


def _minify_svg(task):
    (filename,) = task.file_dep
    (target,) = task.targets

    with open(target, 'wb') as o, open(filename) as i:
        o.write(
            cairosvg.svg2svg(url=filename)
            )

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
    yield {
        'name': 'sass',
        'actions': [_compile_sass],
        'file_dep': ['ballroom_theme/static/css/main.sass'],
        'targets': ['ballroom_theme/static/css/main.css'],
    }

def task_image_files():
    yield {
        'name': 'svg',
        'actions': [_minify_svg],
        'file_dep': ['ballroom_theme/static/img/dancers.svg'],
        'targets': ['ballroom_theme/static/img/dancers.min.svg'],
    }

    yield {
        'name': 'png',
        'actions': [_convert_svg_png],
        'file_dep': ['ballroom_theme/static/img/dancers.svg'],
        'targets': ['ballroom_theme/static/img/dancers.png'],
    }

    yield {
        'name': 'ico',
        'actions': [_convert_png_ico],
        'file_dep': ['ballroom_theme/static/img/dancers.png'],
        'targets': ['ballroom_theme/static/img/dancers.gif'],

    }

def task_pelican():
    yield {
        'name': 'pelican',
        'actions': ['pelican content -s config/local.py -o output'],
        'task_dep': ['image_files', 'sass_files'],
    }
