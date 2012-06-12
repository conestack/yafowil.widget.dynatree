import os
import json
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


def json_response(environ, start_response):
    request = Request(environ)
    selected = request.GET['selected'].split('|')
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
    response = Response(content_type='application/json', body=json.dumps(data))
    return response(environ, start_response)


def isSomethingSelectedInChildren(children, selected):
    return bool(set([_['key'] for _ in children]).intersection(selected)) \
        or bool([_ for _ in children
            if _['children'] and isSomethingSelectedInChildren(_['children'], selected)])


def get_example():
    part = factory(u'fieldset', name='yafowilwidgetdynatree')
    part['local'] = factory('field:label:error:dynatree', props={
        'label': 'Select single value',
        'value': '',
        'source': sample_tree})
    part['remote'] = factory('field:label:error:dynatree', props={
        'label': 'Select multiple',
        'value': '',
        'source': 'yafowil.widget.dynatree.json',
        'selectMode': 2})
    routes = {'yafowil.widget.dynatree.json': json_response}
    return {'widget': part, 'routes': routes}
