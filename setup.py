from setuptools import setup, find_packages
import sys, os

version = '1.3'
shortdesc = 'Tree Selection Widget for YAFOWIL'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()
tests_require = ['interlude', 'lxml', 'yafowil.webob', 'gunicorn', 'simplejson']

setup(name='yafowil.widget.dynatree',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Environment :: Web Environment',
            'Operating System :: OS Independent',
            'Programming Language :: Python', 
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'License :: OSI Approved :: BSD License',
      ],
      keywords='',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url=u'http://github.com/bluedynamics/yafowil.widget.dynatree',
      license='Simplified BSD',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['yafowil', 'yafowil.widget'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'yafowil>=1.3',
      ],
      tests_require=tests_require,
      test_suite="yafowil.widget.dynatree.tests.test_suite",
      extras_require = dict(
          test=tests_require,
      ),
      entry_points="""
      [yafowil.plugin]
      register = yafowil.widget.dynatree:register
      resourcedir = yafowil.widget.dynatree:get_resource_dir
      javascripts = yafowil.widget.dynatree:get_js
      stylesheets = yafowil.widget.dynatree:get_css
      """,           
      )
