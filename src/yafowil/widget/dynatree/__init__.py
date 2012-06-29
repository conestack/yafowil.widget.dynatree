import os
from yafowil.base import factory


resourcedir = os.path.join(os.path.dirname(__file__), 'resources')

js = [{
    'resource': 'jquery.dynatree/jquery.dynatree.min.js',
    'thirdparty': True,
    'order': 20,
}, {
    'resource': 'widget.js',
    'thirdparty': False,
    'order': 21,
}]

default_css = [{
    'resource': 'jquery.dynatree/skin/ui.dynatree.css',
    'thirdparty': True,
    'order': 20,
}, {
    'resource': 'widget.css',
    'thirdparty': False,
    'order': 21,
}]

bootstrap_css = [{
    'resource': 'jquery.dynatree/skin-bootstrap/ui.dynatree.css',
    'thirdparty': True,
    'order': 20,
}, {
    'resource': 'widget.css',
    'thirdparty': False,
    'order': 21,
}]


def register():
    import widget
    factory.register_theme('default', 'yafowil.widget.dynatree',
                           resourcedir, js=js, css=default_css)
    factory.register_theme('bootstrap', 'yafowil.widget.dynatree',
                           resourcedir, js=js, css=bootstrap_css)