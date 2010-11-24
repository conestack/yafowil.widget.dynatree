from yafowil.base import (
    ExtractionError,
    factory,
)
from yafowil.common import input_generic_renderer
from yafowil.utils import tag

def dynatree_renderer(widget, data):
    data.attrs['input_field_type'] = 'text'
    result = input_generic_renderer(widget, data)
    source = widget.attrs['source']
    if callable(source):
        source = source(widget, data)
    if isinstance(source, (list, tuple)):
        source = '|'.join(source)
        source_type = 'local'
    elif isinstance(source, basestring):
        source_type = 'remote'  
    else:
        raise ValueError, 'resulting source must be tuple/list or string'  
    result += tag('div', source, 
                  **{'class': 'dynatree-source hiddenStructure'})
    params = [('%s,%s' % (_, widget.attrs[_])) for _ in ['delay', 'minLength']]
    params.append('type,%s' % source_type)
    result += tag('div', '|'.join(params), 
                  **{'class': 'dynatree-params hiddenStructure'})
    return tag('div', result, **{'class': 'yafowil-widget-dynatree'})

def dynatree_extractor(widget, data):
    #TODO
    return data.extracted

factory.register('dynatree', 
                 [dynatree_extractor], 
                 [dynatree_renderer])
factory.defaults['dynatree.required_class'] = 'required'
factory.defaults['dynatree.delay'] = '300' #ms
factory.defaults['dynatree.minLength'] = '1' #characters