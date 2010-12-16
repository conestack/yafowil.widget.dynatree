==================================
jquery.dynatree widget for YAFOWIL
==================================

A tree-widget for yafowil utilizing the jQuery plugin `jquery.dynatree.js 
<http://wwwendt.de/tech/dynatree/index.html>`_ (at 
`google-code <http://code.google.com/p/dynatree/>`_).

Usage
=====

TODO

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
        ${tests:eggs}
        gunicorn 
    
Start the application with::

    ./bin/gunicorn yafowil.widget.dynatree.example:app

and connect with your webbrowser to ``http://localhost:8000/``
    
Run the tests with::

    ./bin/tests


Contributors
============

- Jens Klein <jens@bluedynamics.com>
