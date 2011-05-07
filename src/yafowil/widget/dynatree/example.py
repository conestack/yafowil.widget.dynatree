import os
from simplejson import dumps
from yafowil import loader
import yafowil.webob
from yafowil.base import factory
from yafowil.controller import Controller
import yafowil.widget.dynatree
from yafowil.tests import fxml
from webob import Request, Response

dir = os.path.dirname(__file__)


sample_tree = {
    'animal': ('Animals', { 
        'mammal': ('Mammals', {
            'elephant': ('Elephant', None),
            'ape': ('Ape', None),
            'horse': ('Horse', None),
        }), 
        'bird': ('Birds', { 
            'duck': ('Duck', None),
            'swan': ('Swan', None),
            'turkey': ('Turkey', None),
            'hummingbird': ('Hummingbird', None),
        }), 
})}


def javascript_response(environ, start_response):
    response = Response(content_type='text/javascript')
    with open(os.path.join(dir, 'resources', 'widget.js')) as js:
        response.write(js.read())
    return response(environ, start_response)


def javascript_response2(environ, start_response):
    response = Response(content_type='text/javascript')
    with open(os.path.join(dir, 'resources', 'jquery.dynatree', 
                           'jquery.dynatree.js')) as js:
        response.write(js.read())
    return response(environ, start_response)


def skin_response(environ, start_response):
    if environ['PATH_INFO'].endswith('.gif'):        
        response = Response(content_type='image/gif')
    elif environ['PATH_INFO'].endswith('.css'):        
        response = Response(content_type='text/css')
    with open(os.path.join(dir, 'resources', 'jquery.dynatree', 
                           environ['PATH_INFO'].strip('/'))) as item:
        response.write(item.read())
    return response(environ, start_response)


def json_response(environ, start_response):
    request = Request(environ)
    selected = request.str_GET['selected'].split('|')    
    def dir_tree(base):
        result = []
        for value in os.listdir(base):
            if value.endswith('pyc') or value.startswith('.'):
                continue
            new_item = {} #we have to have boolItems
            new_item['key'] = os.path.join(base, value) 
            new_item['title'] = value
            new_item['children'] = []
            if os.path.isdir(new_item['key']):
                new_item['children'] = dir_tree(new_item['key'])
            new_item['select'] = new_item['key'] in selected
            new_item['isFolder'] = bool(new_item['children'])
            new_item['hideCheckbox'] = False
            new_item['expand'] = new_item['key'] in selected \
                          or isSomethingSelectedInChildren(new_item['children'], 
                                                           selected)
            result.append(new_item)
        return result                                              
    data = dir_tree(dir)
    response = Response(content_type='application/json', body=dumps(data))
    return response(environ, start_response)


def isSomethingSelectedInChildren(children, selected):
    return bool(set([_['key'] for _ in children]).intersection(selected)) \
        or bool([_ for _ in children
            if _['children'] and isSomethingSelectedInChildren(_['children'], selected)])


def app(environ, start_response):
    url = 'http://%s/' % environ['HTTP_HOST']
    if environ['PATH_INFO'] == '/ywd.js':
        return javascript_response(environ, start_response)
    elif environ['PATH_INFO'] == '/ywd.json':
        return json_response(environ, start_response)
    elif environ['PATH_INFO'] == '/jquery.dynatree.js':
        return javascript_response2(environ, start_response)
    elif environ['PATH_INFO'].startswith('/skin/'):
        return skin_response(environ, start_response)
    elif environ['PATH_INFO'] != '/':
        response = Response(status=404)
        return response(environ, start_response)
    form = factory(u'form', name='yqaexample', props={
        'action': url})
    form['local'] = factory('field:label:error:dynatree', props={
        'label': 'Select single value',
        'value': '',
        'source': sample_tree})
    form['remote'] = factory('field:label:error:dynatree', props={
        'label': 'Select multiple',
        'value': '',
        'source': '%sywd.json' % url,
        'selectMode': 2})
    form['submit'] = factory('field:submit', props={        
        'label': 'submit',
        'action': 'save',
        'handler': lambda widget, data: None,
        'next': lambda request: url})
    controller = Controller(form, Request(environ))
    tag = controller.data.tag
    jq = tag('script', ' ',
             src='https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.js',
             type='text/javascript')
    jqui = tag('script', ' ', 
               src='https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.js',
               type='text/javascript')
    jqdy = tag('script', ' ',
              src='%sjquery.dynatree.js' % url,
              type='text/javascript')    
    ywd = tag('script', ' ',
              src='%sywd.js' % url,
              type='text/javascript')    
    css = tag("style",
              "@import url(%sskin/ui.dynatree.css)" % url,
              type='text/css')
    css += tag('style',
              '.hiddenStructure { display: none; }', 
              type='text/css')
    head = tag('head', jq, jqui, jqdy, ywd, css)
    h1 = tag('h1', 'YAFOWIL Widget Dynatree Example')
    body = tag('body', h1, controller.rendered)
    response = Response(body=fxml(tag('html', head, body)))
    return response(environ, start_response)