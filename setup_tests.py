r"""Speclenium-tests
The Speclenium test suite.
"""
import sys, os
from distutils.core import setup, Command, DistutilsOptionError
from distutils.archive_util import make_archive
import distutils.command, distutils.command.build_py
import shutil
import tests, selenium, specular

class standalone(distutils.command.build_py.build_py):
    description = "Create a standalone speclenium test suite and harness."
    user_options = \
        [('formats=','F','formats for distribution (comma-seperated list)')]+\
        distutils.command.build_py.build_py.user_options
    def initialize_options(self):
        distutils.command.build_py.build_py.initialize_options(self)
        self.dist_dir = None
        if sys.platform == 'win32':
            self.formats = 'zip'
        else:
            self.formats = 'gztar'

    def finalize_options(self):
        distutils.command.build_py.build_py.finalize_options(self)
        if self.dist_dir is None:
            self.dist_dir = "dist"
        self.filelist = \
            [(m[2], os.path.dirname(m[2])) for m in self.find_all_modules()]
        self.filelist.append((selenium.__file__.rstrip('c'), ""))
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


distutils.command.__all__ = []
distutils.command.__all__.append('standalone')

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
      packages=["tests"],
      scripts=["run_tests"], 
      data_files=[('', ['LICENSE', 'settings.ini'])], **extras)
