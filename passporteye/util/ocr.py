'''
PassportEye::Util: Interface between SKImage and the PyTesseract OCR
NB: You must have the "tesseract" tool present in your path for this to work.

Author: Konstantin Tretyakov
License: MIT
'''

import tempfile
import numpy as np
from imageio import imwrite
from pytesseract import pytesseract


def ocr(img, mrz_mode=True, extra_cmdline_params=''):
    """Runs Tesseract on a given image. Writes an intermediate tempfile and then runs the tesseract command on the image.

    This is a simplified modification of image_to_string from PyTesseract, which is adapted to SKImage rather than PIL.

    In principle we could have reimplemented it just as well - there are some apparent bugs in PyTesseract, but it works so far :)

    :param mrz_mode: when this is True (default) the tesseract is configured to recognize MRZs rather than arbitrary texts.
                     When False, no specific configuration parameters are passed (and you are free to provide your own via `extra_cmdline_params`)
    :param extra_cmdline_params: extra parameters passed to tesseract. When mrz_mode=True, these are appended to whatever is the
                    "best known" configuration at the moment.
                    "--oem 0" is the parameter you might want to pass. This selects the Tesseract's "legacy" OCR engine, which often seems
                    to work better than the new LSTM-based one.
    """
    if img is None or img.shape[-1] == 0:  # Issue #34
        return ''
    input_file_name = '%s.bmp' % _tempnam()
    output_file_name_base = '%s' % _tempnam()
    output_file_name = "%s.txt" % output_file_name_base
    try:
        # Prevent annoying warning about lossy conversion to uint8
        if str(img.dtype).startswith('float') and np.nanmin(img) >= 0 and np.nanmax(img) <= 1:
            img = img.astype(np.float64) * (np.power(2.0, 8) - 1) + 0.499999999
            img = img.astype(np.uint8)
        imwrite(input_file_name, img)

        if mrz_mode:
			# NB: Tesseract 4.0 does not seem to support tessedit_char_whitelist
            config = ("--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789><"
                      " -c load_system_dawg=F -c load_freq_dawg=F {}").format(extra_cmdline_params)
        else:
            config = "{}".format(extra_cmdline_params)

        pytesseract.run_tesseract(input_file_name,
                                  output_file_name_base,
                                  'txt',
                                  lang=None,
                                  config=config)
        
        f = open(output_file_name, encoding='utf-8')
        
        try:
            return f.read().strip()
        finally:
            f.close()
    finally:
        pytesseract.cleanup(input_file_name)
        pytesseract.cleanup(output_file_name)


def _tempnam():
    '''TODO: Use the with(..) version for auto-deletion?'''
    tmpfile = tempfile.NamedTemporaryFile(prefix="tess_")
    return tmpfile.name
