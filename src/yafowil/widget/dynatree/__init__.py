import os 

def register():
    import widget
    
def get_resource_dir():
    return os.path.join(os.path.dirname(__file__), 'resources')
        
def get_js(thirdparty=True):
    js = ['widget.js']
    if thirdparty:
        js.append['jquery.dynatree/jquery.dynatree.min.js']
    return js

def get_css(thirdparty=True):
    if thirdparty:
        return ['jquery.dynatree/skin/ui.dynatree.css']
    return []