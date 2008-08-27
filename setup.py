r"""Specular
A cross-platform accessibility API inspection library and service.
"""
import sys, os
from distutils.core import setup, Command, DistutilsOptionError
from distutils.archive_util import make_archive
import distutils.command
import shutil
import specular

options = {}


class _include_selenium:
    user_options = [('selenium=', 'S', 'Selenium JAR file to include')]
    def initialize_options(self):
        self.selenium = 'selenium-server.jar'
    def finalize_options(self):
        if self.distribution.data_files is None:
            self.distribution.data_files = []
        self.distribution.data_files.append(('', [self.selenium]))
        

try:
    import py2exe
except ImportError:
    # Not on windows or no py2exe, no biggie.
    extras = {}
else:
    class standalone_win32(py2exe.build_exe.py2exe, _include_selenium):
        user_options = py2exe.build_exe.py2exe.user_options + \
            _include_selenium.user_options + \
            [('zip', 'Z', 'zip distribution')]

        def initialize_options(self):
            self.zip = False
            _include_selenium.initialize_options(self)
            py2exe.build_exe.py2exe.initialize_options(self)

        def finalize_options(self):
            _include_selenium.finalize_options(self)
            py2exe.build_exe.py2exe.finalize_options(self)
            if self.zip:
                self.base_name = \
                    self.distribution.get_fullname().lower()
                self.archive_dir = os.path.join(self.dist_dir, self.base_name)
                self.base_dir = self.dist_dir
                self.dist_dir = self.archive_dir
                os.makedirs(self.dist_dir)

        def run(self):
            py2exe.build_exe.py2exe.run(self)
            if self.zip:
                archive_name = make_archive(self.base_name + '.win32', 'zip', 
                                             self.base_dir, self.base_name)
                print
                print 'Created', archive_name
                shutil.rmtree(self.archive_dir)
                print 'Deleted', self.archive_dir

    extras = {'options' : {'bdist_win32_standalone' : 
                           {'includes' : 'twisted.web.resource'}},
              'console' : [{'script' : 'speclenium',
                            "icon_resources" : 
                            [(1, "pixmaps/speclenium-logo.ico")]}],
              'cmdclass' : {'standalone_win32' : standalone_win32}}


classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: Microsoft :: Windows'
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
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
      packages=["specular", "specular.speclenium"],
      scripts=["speclenium"], **extras)
