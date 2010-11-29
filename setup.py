from setuptools import setup, find_packages
import sys, os

version = '1.0'
shortdesc = 'Autocomplete Widget for YAFOWIL - Yet Another Form Widget Library (Python, Web)'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()
tests_require = ['interlude', 'lxml', 'yafowil.webob', 'gunicorn', 'simplejson']

setup(name='yafowil.widget.dynatree',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Operating System :: OS Independent',
            'Programming Language :: Python', 
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',        
      ],
      keywords='',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url=u'http://github.com/bluedynamics/yafowil.widget.dynatree',
      license='GNU General Public Licence',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['yafowil', 'yafowil.widget'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'yafowil',
      ],
      tests_require=tests_require,
      test_suite="yafowil.widget.dynatree.tests.test_suite",
      extras_require = dict(
          test=tests_require,
      ),
      entry_points = """\
      """        
      )
