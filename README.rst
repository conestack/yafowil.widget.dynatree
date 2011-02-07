This is a **tree widget** for `YAFOWIL 
<http://pypi.python.org/pypi/yafowil>`_ - Yet Another Form WIdget Library.

The tree-widget for yafowil utilizes the jQuery plugin `jquery.dynatree.js 
<http://wwwendt.de/tech/dynatree/index.html>`_ (at 
`google-code <http://code.google.com/p/dynatree/>`_).


Usage
=====

The dynatree widget takes the parameters:

- source
- selectMode
- minExpandLevel
- rootVisible
- autoCollapse
- checkbox'

For details read the `Dynatree Widget Documentation 
<http://packages.python.org/yafowil/widgets.html#dynatree>`_ 
    
Example::

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
    form['mytree'] = factory('dynatree', props={
        'value': ['ape', 'bird'],
        'source': sample_tree,
    )
    
Further `yafowil.dynatree documentation 
<http://packages.python.org/yafowil/widgets.html#dynatree>`_  is available


Example Application
===================

To run the example application and tests coming with this package run 
`bootstrap <http://python-distribute.org/bootstrap.py>`_ (Python 2.6 or 2.7) 
with a buildout like so:: 

    [buildout]
    parts = gunicorn   
    
    [tests]
    recipe = zc.recipe.testrunner
    eggs = 
        yafowil.widget.dynatree[test]
    
    [gunicorn]
    recipe = zc.recipe.egg:scripts
    eggs = 
        ${test:eggs}
        gunicorn 
    
Start the application with::

    ./bin/gunicorn yafowil.widget.dynatree.example:app

and connect with your webbrowser to ``http://localhost:8000/``
    
Run the tests with::

    ./bin/tests    


Source Code
===========

The sources are in a GIT DVCS with its main branches at 
`github <http://github.com/bluedynamics/yafowil.widget.dynatree>`_.

We'd be happy to see many forks and pull-requests to make YAFOWIL even better.


Contributors
============

- Jens Klein <jens@bluedynamics.com>
