from yafowil.base import (
    ExtractionError,
    factory,
    UNSET,
)
from yafowil.utils import (
    tag,
    cssid   
)
from yafowil.common import (
    input_generic_renderer,
    generic_extractor,
    generic_required_extractor
)

def build_inline_dynatree(tree, selected, ulid=None):
    if tree is None: return ''
    li = ''
    for key in tree:
        title, subtree = tree[key]
        # TODO: handle all the parameters
        li += tag('li', title, build_inline_dynatree(subtree, selected), 
                  '\n',
                  **{'id': key})
    ul_attrs = dict()
    if ulid is not None:
        ul_attrs['id'] = ulid
        ul_attrs['class'] = 'hiddenStructure'
    return tag('ul',  '\n', li, **ul_attrs)

def dynatree_renderer(widget, data):
    data.attrs['input_field_type'] = 'hidden'
    result = input_generic_renderer(widget, data)
    source = widget.attrs['source']
    if callable(source):
        source = source(widget, data)
    if isinstance(source, dict):        
        source_type = 'local'
        ulid = cssid(widget, 'dynatree-source');
        result += build_inline_dynatree(source, data.value, ulid=ulid)        
    elif isinstance(source, basestring):
        source_type = 'remote'  
        result += tag('div', source, 
                      **{'class': 'dynatree-source hiddenStructure'})
    else:
        raise ValueError, 'resulting source must be [o]dict or string'
    p_keys = ['selectMode', 'minExpandLevel', 'rootVisible', 'autoCollapse', 
              'checkbox']
    params = [('%s,%s' % (_, widget.attrs[_])) for _ in p_keys]    
    params.append('type,%s' % source_type)
    if source_type == 'local':
        params.append(('initId,%s' % ulid))
    result += tag('div', '|'.join(params), 
                  **{'class': 'dynatree-params hiddenStructure'})
    result += tag('div', **{'class': 'yafowil-widget-dynatree-tree'})
    return tag('div', result, **{'class': 'yafowil-widget-dynatree'})

def dynatree_extractor(widget, data):
    if data.extracted is UNSET:
        return data.extracted
    if widget.attrs['selectMode'] == 1:
        return data.extracted.strip('|')
    value = [_ for _ in data.extracted.split('|')if _]
    return value

factory.register('dynatree', 
                 [generic_extractor, 
                  generic_required_extractor,
                  dynatree_extractor], 
                 [dynatree_renderer])

factory.document['dynatree'] = """\
    A tree-widget utilizing the jQuery plugin `jquery.dynatree.js 
    <http://wwwendt.de/tech/dynatree/index.html>`_ (at 
    `google-code <http://code.google.com/p/dynatree/>`_).
"""

factory.document['dynatree.source'] = """\
    The vocabulary source. This can be either [o]dict, string or a a callable
    returning one of both. 
    
    If a dict is passed or returned by the callable, the vocabulary is rendered 
    inline. The dict keys are used as values, dicts value is a tuple of (title, 
    children), where title is shown in the tree and children is either None or 
    a dict of the same structure. 
    
    If a string is passed it is considered as an URL to fetch the vocabulay
    from. It is returned as JSON in the format described in the original
    jquery.dynatreee.js documentation.
    
    If a callable is passed it expects widget and data as parameters and has to 
    return either a string or a dict as described above."""

factory.defaults['dynatree.required_class'] = 'required'

factory.defaults['dynatree.selectMode'] = '1'
factory.document['dynatree.selectMode'] = """\
    1=single selection, 2=multiple selection, 3=multi-hier-mode. In single
    selection mode expected value is a string, in other modes a iterable of
    strings."""

factory.defaults['dynatree.minExpandLevel'] = '1'
factory.document['dynatree.minExpandLevel'] = """\ 
    Number of levels which are not allowed to collapse."""

factory.defaults['dynatree.rootVisible'] = False 
factory.document['dynatree.rootVisible'] = """\
    Wether a root node is shown or not."""
    
factory.defaults['dynatree.autoCollapse'] = False
factory.document['dynatree.autoCollapse'] = """\
    Automatically collapse all siblings, when another node is expanded."""

factory.defaults['dynatree.leafsOnly'] = False
factory.document['dynatree.leafsOnly'] = """\
    Wether to select only leafs or allow also to select nodes with leafs."""

factory.defaults['dynatree.checkbox'] = True
factory.document['dynatree.checkbox'] = """\
    Wether to show checkboxes or not."""    