'''
PassportEye::Util: Interface between SKImage and the PyTesseract OCR
NB: You must have the "tesseract" tool present in your path for this to work.

Author: Konstantin Tretyakov
License: MIT
'''

import sys
import tempfile
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
    """
    input_file_name = '%s.bmp' % _tempnam()
    output_file_name_base = '%s' % _tempnam()
    output_file_name = "%s.txt" % output_file_name_base
    try:
        imwrite(input_file_name, img)

        if mrz_mode:
			# NB: Tesseract 4.0 does not seem to support tessedit_char_whitelist
            # NB: --oem 0 selects the "legacy" engine, which seems to do much better on MRZs than the new one
            config = "--oem 0 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789>< -c load_system_dawg=F -c load_freq_dawg=F {}".format(extra_cmdline_params)
        else:
            config = "{}".format(extra_cmdline_params)

        pytesseract.run_tesseract(input_file_name,
                                 output_file_name_base,
                                 'txt',
                                 lang=None,
                                 config=config)
        
        if sys.version_info.major == 3:
            f = open(output_file_name, encoding='utf-8')
        else:
            f = open(output_file_name)
        
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
