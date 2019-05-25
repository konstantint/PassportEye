'''
Test module for use with py.test.
Write each test as a function named test_<something>.
Read more here: http://pytest.org/

Author: Konstantin Tretyakov
License: MIT
'''
from pkg_resources import resource_filename
import numpy as np
from skimage.io import imread
from passporteye.util.ocr import ocr


# Smoke test for Tesseract OCR
def test_ocr():
    ocr_file = lambda fn, mode: ocr(imread(resource_filename('tests', 'data/%s' % fn)), mode)

    s = ocr_file('tesseract-test1.jpg', False)
    assert s.startswith('The (quick) [brown] {fox} jumps!\nOver the $43,456.78 <lazy> #90 dog\n')
    assert s.endswith('preguicoso.') or s.endswith('preguieoso.') or s.endswith('preguigoso.') # NB: This actually depends on the version of Tesseract

    s = ocr_file('tesseract-test2.png', False)
    assert s.startswith('This is a lot of 12 point text to test the\nocr code and see if') or \
           s.startswith('This is a lot of 12 point text to test the\ncor code and see if')
    assert s.endswith('The quick\nbrown dog jumped over the lazy fox.')

	# Since Tesseract 4.0 this test does not work, at least I did not find the way to limit the output character set
    #s = ocr_file('tesseract-test1.jpg', True)
    #assert s.startswith('T116 10111610 1111011111 110111') or s.startswith('T116 111111610 1111011111 110111')

def test_issue34():
	ocr(np.asarray([]))
	ocr(np.asarray([[]]))
	ocr(np.asarray([[0]], dtype=np.uint8))