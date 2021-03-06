"""Specular
A cross-platform accessibility API inspection service.
"""
import sys, os
from distutils.core import setup, Command
from distutils.archive_util import make_archive
import distutils.command, distutils.command.build_py
import shutil
import specular, speclenium, speclenium_client

class partial_dist(distutils.command.build_py.build_py):
    description = "Create a standalone speclenium test suite and harness."
    user_options = \
        [('formats=','F','formats for distribution (comma-separated list)')]+\
        distutils.command.build_py.build_py.user_options
    dist_overlay = {}

    def __init__(self, dist):
        dist.__dict__.update(self.dist_overlay)
        dist.metadata.__dict__.update(
            dict(filter(lambda x: hasattr(dist.metadata, x[0]), 
                        self.dist_overlay.items())))        
        distutils.command.build_py.build_py.__init__(self, dist)

    def initialize_options(self):
        self.dist_dir = 'dist'
        distutils.command.build_py.build_py.initialize_options(self)
        if sys.platform == 'win32':
            self.formats = 'zip'
        else:
            self.formats = 'gztar'

    def finalize_options(self):
        distutils.command.build_py.build_py.finalize_options(self)
        self.filelist = \
            [(m[2], os.path.dirname(m[2])) for m in self.find_all_modules()]
        self.filelist += [(s, "") for s in self.distribution.scripts]
        for dest, data_files in self.distribution.data_files:
            for f in data_files:
                self.filelist.append((f, dest))

    def run(self):
        dest_root = \
            os.path.join(self.dist_dir,self.distribution.get_fullname())
        self.mkpath(dest_root)
        for f, dest_dir in self.filelist:
            dest_dir = os.path.join(dest_root, dest_dir)
            dest_file = os.path.join(dest_dir, os.path.basename(f))
            if not os.path.exists(dest_dir):
                self.mkpath(dest_dir)
            self.copy_file(f, dest_file)
            if f in self.distribution.scripts:
                print 'changing mode of', dest_file
                os.chmod(dest_file, 493)

        for fmt in self.formats.split(','):
            self.make_archive(
                os.path.join(self.dist_dir, self.distribution.get_fullname()), 
                fmt, self.dist_dir, self.distribution.get_fullname())
        shutil.rmtree(dest_root)

class speclenium_dist(partial_dist):
    description = "Create a standalone speclenium test suite and harness."
    user_options = [('speclenium_client=', 'S', 'Selenium JAR file to include')] + \
        partial_dist.user_options
    dist_overlay = dict(
        name='Speclenium-standalone',
        data_files=[('', ['LICENSE', 'README', 'README.speclenium', ])],
        packages=['specular', 'speclenium'],
        scripts=['speclenium_server.py'])

    def initialize_options(self):
        self.speclenium_client = "speclenium_client-server.jar"
        partial_dist.initialize_options(self)

    def finalize_options(self):
        self.distribution.__dict__.setdefault('data_files', []).append(
            ('', [self.speclenium_client]))
        partial_dist.finalize_options(self)

class testsuite_dist(partial_dist):
    description = "Create a standalone speclenium test suite and harness."
    selenium_file_name = speclenium_client.__file__
    dist_overlay = dict(
        name=__doc__.split('\n')[0]+'-testsuite',
        data_files=[('', ['LICENSE', 'README', 'README.tests', 
                          'README.api_diff','settings.ini',
                          selenium_file_name.rstrip('c')]),
                    ('viewdiff', ['viewdiff/api-compare.css', 
                                  'viewdiff/api-compare.js', 
                                  'viewdiff/api-compare.xsl'])],
        packages=['tests', 'treediff'],
        py_modules=['speclenium_client'],
        scripts=['run_tests.py', 'quick_diff.py'])

try:
    import py2exe
except ImportError:
    # Not on windows or no py2exe, no biggie.
    extras = {'cmdclass' : {'testsuite_dist' : testsuite_dist,
                            'speclenium_dist' : speclenium_dist}}
else:
    class speclenium_dist_win32(py2exe.build_exe.py2exe):
        description = \
            "Create a standalone speclenium distribution for Windows."
        user_options = py2exe.build_exe.py2exe.user_options + \
            [('zip', 'Z', 'zip distribution'),
             ('speclenium_client=', 'S', 'Selenium JAR file to include')]

        def __init__(self, dist):
            dist.metadata.name = dist.name = 'Speclenium-standalone-win32'
            dist.data_files=[('', ['LICENSE', 
                                   'README', 
                                   'README.speclenium'])]
            py2exe.build_exe.py2exe.__init__(self, dist)

        def initialize_options(self):
            self.zip = False
            self.speclenium_client = 'speclenium_client-server.jar'
            py2exe.build_exe.py2exe.initialize_options(self)

        def finalize_options(self):
            if self.distribution.data_files is None:
                self.distribution.data_files = []
            self.distribution.data_files.append(('', [self.speclenium_client]))
            py2exe.build_exe.py2exe.finalize_options(self)
            self.base_name = \
                self.distribution.get_fullname()
            self.archive_dir = os.path.join(self.dist_dir, self.base_name)
            self.base_dir = self.dist_dir
            self.dist_dir = self.archive_dir
            os.makedirs(self.dist_dir)

        def run(self):
            py2exe.build_exe.py2exe.run(self)
            if self.zip:
                archive_name = make_archive(
                    os.path.join(self.dist_dir, self.base_name),
                    'zip', self.base_dir, self.base_name)
                shutil.rmtree(self.archive_dir)

    extras = {'options' : {'speclenium_dist_win32' : 
                           {'includes' : 'twisted.web.resource'}},
              'console' : [{'script' : 'speclenium_server.py',
                            "icon_resources" : 
                            [(1, "speclenium-logo.ico")]}],
              'cmdclass' : {'testsuite_dist' : testsuite_dist,
                            'speclenium_dist_win32' : speclenium_dist_win32,
                            'speclenium_dist' : speclenium_dist}}


classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: Microsoft :: Windows'
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Software Development :: Testing', 
    'Topic :: Software Development :: Quality Assurance'
    ]


setup(name=__doc__.split('\n')[0],
      description=__doc__.split('\n')[1],
      long_description = __doc__.split('\n')[1],
      author="Eitan Isaacson",
      author_email="eitan@ascender.com",
      url="http://monotonous.org",
      download_url = "",
      license=specular.__license__,
      classifiers=classifiers,
      version=specular.__version__,
      packages=["specular", "speclenium", "tests"],
      py_modules=["speclenium_client"],
      scripts=["speclenium_server.py", "run_tests.py"], 
      data_files=[('', ['LICENSE', 
                        'README', 
                        'README.speclenium',
                        'README.api_diff', 
                        'README.tests'])],
      **extras)
