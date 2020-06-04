'''
PassportEye: Python tools for image processing of identification documents

Author: Konstantin Tretyakov
License: MIT
'''
import sys
from setuptools import setup, find_packages


setup(name='PassportEye',
      version=[ln for ln in open("passporteye/__init__.py") if ln.startswith("__version__")][0].split('"')[1],
      description="Extraction of machine-readable zone information from passports, visas and id-cards via OCR",
      long_description=open("README.rst").read(),
      classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
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
      install_requires=['numpy', 'scipy', 'scikit-image >= 0.14.1', 'imageio', 'scikit-learn', 'matplotlib', 'pytesseract >= 0.2.0', 'imageio',
                        'pdfminer'],
      extras_require={
          "test": ["pytest"],
          "dev": ["pytest", "pylint", "jupyter", "twine"],
      },
      entry_points={
          'console_scripts': ['evaluate_mrz=passporteye.mrz.scripts:evaluate_mrz',
                              'mrz=passporteye.mrz.scripts:mrz']
      }
     )
