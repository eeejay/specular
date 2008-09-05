r"""Speclenium
A cross-platform accessibility API inspection service.
"""
import sys, os
from distutils.core import setup, Command, DistutilsOptionError
from distutils.archive_util import make_archive
import distutils.command, distutils.command.build_py
import shutil
import specular, specular.speclenium

class standalone(distutils.command.build_py.build_py):
    description = "Create a standalone speclenium distribution."
    user_options = [('selenium=', 'S', 'Selenium JAR file to include')] + \
        distutils.command.build_py.build_py.user_options
    
    def initialize_options(self):
        distutils.command.build_py.build_py.initialize_options(self)
        self.selenium = 'selenium-server.jar'
        self.dist_dir = None

    def finalize_options(self):
        distutils.command.build_py.build_py.finalize_options(self)
        if self.dist_dir is None:
            self.dist_dir = "dist"
        self.filelist = \
            [(m[2], os.path.dirname(m[2])) for m in self.find_all_modules()]
        self.filelist.append((self.selenium, ""))
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

        archive_name = \
            self.make_archive(
                os.path.join(self.dist_dir, self.distribution.get_fullname()), 
                'gztar', self.dist_dir, self.distribution.get_fullname())
        shutil.rmtree(dest_root)


distutils.command.__all__ = []
distutils.command.__all__.append('standalone')

try:
    import py2exe
except ImportError:
    # Not on windows or no py2exe, no biggie.
    extras = {'cmdclass' : {'standalone' : standalone}}
else:
    class standalone_win32(py2exe.build_exe.py2exe, _include_selenium):
        description = \
            "Create a standalone speclenium distribution for Windows."
        user_options = py2exe.build_exe.py2exe.user_options + \
            _include_selenium.user_options + \
            [('zip', 'Z', 'zip distribution'),
             ('selenium=', 'S', 'Selenium JAR file to include')]

        def initialize_options(self):
            self.zip = False
            self.selenium = 'selenium-server.jar'
            py2exe.build_exe.py2exe.initialize_options(self)

        def finalize_options(self):
            if self.distribution.data_files is None:
                self.distribution.data_files = []
            self.distribution.data_files.append(('', [self.selenium]))
            py2exe.build_exe.py2exe.finalize_options(self)
            if self.zip:
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
                    os.path.join(self.dist_dir, self.base_name + '.win32'),
                    'zip', self.base_dir, self.base_name)
                shutil.rmtree(self.archive_dir)

    distutils.command.__all__.append('standalone_win32')

    extras = {'options' : {'standalone_win32' : 
                           {'includes' : 'twisted.web.resource'}},
              'console' : [{'script' : 'speclenium',
                            "icon_resources" : 
                            [(1, "pixmaps/speclenium-logo.ico")]}],
              'cmdclass' : {'standalone_win32' : standalone_win32,
                            'standalone' : standalone}}


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
      scripts=["speclenium"], 
      data_files=[('', ['LICENSE'])], **extras)
