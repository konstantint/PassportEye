'''
PassportEye: Python tools for image processing of identification documents

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

Author: Konstantin Tretyakov
License: MIT
'''
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))

setup(name='PassportEye',
      version=[ln for ln in open("passporteye/__init__.py") if ln.startswith("__version__")][0].split('"')[1],
      description="Extraction of machine-readable zone information from passports, visas and id-cards via OCR",
      long_description=open("README.rst").read(),
      classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Financial and Insurance Industry'
      ],
      keywords='id-card passport image-processing mrz machine-readable-zone',
      author='Konstantin Tretyakov',
      author_email='kt@ut.ee',
      url='https://github.com/konstantint/PassportEye',
      license='MIT',
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['pdfminer', 'numpy', 'scipy', 'scikit-image >= 0.12.1', 'scikit-learn', 'matplotlib', 'pytesseract'],
      entry_points={
          'console_scripts': ['evaluate_mrz=passporteye.mrz.scripts:evaluate_mrz',
                              'mrz=passporteye.mrz.scripts:mrz']
      }
)
