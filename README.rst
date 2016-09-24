==========================================================================
PassportEye: Python tools for image processing of identification documents
==========================================================================

The package provides tools for recognizing machine readable zones (MRZ) from scanned identification documents.
The documents may be located rather arbitrarily on the page - the code tries to find anything resembling a MRZ 
and parse it from there.

The recognition procedure may be rather slow - around 10 or more seconds for some documents. Its precision is
not perfect, yet seemingly decent as far as test documents available to the developer were concerned - in
around 80% of the cases, whenever there is a clearly visible MRZ on a page, the system will recognize it and extract the text
to the best of the abilities of the underlying OCR engine (Google Tesseract).

The failed examples seem to be most often either clearly badly scanned documents, where text is way too blurred, or,
more seriously, some types of IDs (Romanian being one example), where the MRZ is too close to the remaining part of the card - 
a situation not accounted for too well by the current algorithm.

Installation
------------

The simplest way to install the package is via ``easy_install`` or
``pip``::

    $ pip install PassportEye

Note that `PassportEye` depends on `numpy`, `scipy`, `matplotlib` and `scikit-image`, among other things. The installation of those requirements, although automatic,
may take time or fail sometimes for various reasons (e.g. lack of necessary libraries). If this happens, consider installing the dependencies explicitly from the binary packages, such as those provided by the OS distribution or the "wheel" packages. Another convenient option is to use a Python distribution with pre-packaged `numpy`/`scipy`/`matplotlib` binaries (Anaconda Python being a great choice at the moment).

In addition, you must have the `Tesseract OCR <https://github.com/tesseract-ocr>`_ installed and added to the system path: the ``tesseract`` tool must be 
accessible at the command line.

Usage
-----

On installation, the package installs a standalone tool ``mrz`` into your Python scripts path. Running::

    $ mrz <filename>
    
will process a given filename, extracting the MRZ information it finds and printing it out in tabular form.
Running ``mrz --json <filename>`` will output the same information in JSON. Running ``mrz --save-roi <roi.png>`` will,
in addition, extract the detected MRZ ("region of interest") into a separate png file for further exploration.
Note that the tool provides a limited support for PDF files -- it attempts to extract the first DCT-encoded image 
from the PDF and applies the recognition on it. This seems to work fine with most scanner-produced one-page PDFs, but
has not been tested extensively.

In order to use the recognition function in Python code, simply do::

    >> from passporteye import read_mrz
    >> mrz = read_mrz(image_filename)

The returned object (unless it is None, which means no ROI was detected) contains the fields extracted from the MRZ along
with some metainformation. For the description of the available fields, see the docstring for the `passporteye.mrz.text.MRZ` class.
Note that you can convert the object to a dictionary using the ``to_dict()`` method.

If you want to have the ROI reported alongside the MRZ, call the ``read_mrz`` function as follows::

    >> mrz = read_mrz(image_filename, save_roi=True)

The ROI can then be accessed as ``mrz.aux['roi']`` -- it is a numpy ndarray, representing the (grayscale) image region where the OCR was applied.

For more flexibility, you may instead use a ``MRZPipeline`` object, which will provide you access to all intermediate computations as follows::

    >> from passporteye.mrz.image import MRZPipeline
    >> p = MRZPipeline(filename)
    >> mrz = p.result

The "pipeline" object stores the intermediate computations in its ``data`` dictionary. Although you need to understand the underlying algorithm
to make sense of it, sometimes it may provide for insightful visualizations. This code, for example, will plot the binarized version of the original image
which is used in the algorithm to extract ROIs alongside the boxes corresponding to the extracted ROIs::

    >> imshow(p['img_binary'])
    >> for b in p['boxes']:
    ..     plot(b.points[:,1], b.points[:,0], c='b')
    ..     b.plot()

Development
-----------

If you plan to develop or debug the package, consider installing it by running::

    $ python setup.py develop

from within the source distribution. The package contains a basic set of smoke tests. To run those you should first make sure you have
`pytest` installed::

    $ pip install pytest

You can then run the tests by typing::

    $ py.test
    
At the root of the source distribution.

The command-line script ``evaluate_mrz`` can be used to assess the performance of the current recognition pipeline on a set 
of sample images: this is useful if you want to see the effects of changes to the code. Just run::

    $ evaluate_mrz -j 4

(where ``-j 4`` would request to use 4 cores in parallel). The same script may be used to run the recognition pipeline on a 
given directory of images, sorting successes and failures, see ``evaluate_mrz -h`` for options.


Contributing
------------

Feel free to contribute or report issues via Github: https://github.com/konstantint/PassportEye

Copyright & License
-------------------

Copyright: 2016, Konstantin Tretyakov.
License: MIT
