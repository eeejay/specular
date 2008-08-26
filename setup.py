r"""Specular
A cross-platform accessibility API inspection library and service.
"""
import sys, os
from distutils.core import setup, Command, DistutilsOptionError
import distutils.command
import shutil
import specular

options = {}

try:
    import py2exe
except ImportError:
    # Not on windows or no py2exe, no biggie.
    extras = {}
else:
    class bdist_win32_standalone(py2exe.build_exe.py2exe):
        user_options = py2exe.build_exe.py2exe.user_options + \
            [('selenium=', 'S', 'Selenium JAR file to include')]

        def initialize_options(self):
            self.selenium = 'selenium-server.jar'
            py2exe.build_exe.py2exe.initialize_options(self)

        def finalize_options(self):
            if not os.path.exists(self.selenium):
                raise DistutilsOptionError, \
                    'Cannot find "%s". ' \
                    'Use -S to point to a selenium server JAR file.' \
                        % self.selenium
            py2exe.build_exe.py2exe.finalize_options(self)

        def run(self):
            py2exe.build_exe.py2exe.run(self)
            print 
            print 'Copying', self.selenium, 'to', self.dist_dir
            shutil.copy(self.selenium, 
                        os.path.join(self.dist_dir, 'selenium-server.jar'))

    extras = {'options' : {'bdist_win32_standalone' : 
                           {'includes' : 'twisted.web.resource'}},
              'console' : ['speclenium'],
              'cmdclass' : {'bdist_win32_standalone' : bdist_win32_standalone}}


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
