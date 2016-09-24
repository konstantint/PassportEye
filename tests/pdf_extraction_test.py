'''
Test module for use with py.test.
Write each test as a function named test_<something>.
Read more here: http://pytest.org/

Author: Konstantin Tretyakov
License: MIT
'''
from pkg_resources import resource_filename
from passporteye.util.pdf import extract_first_jpeg_in_pdf


# Smoke test for "extract_first_jpeg_in_pdf"
def test_extract_jpeg():
    for fn, has_image in [('pdf-with-jpg.pdf',True),
                          ('pdf-with-png.pdf',False),
                          ('pdf-with-pngjpg.pdf',True),
                          ('pdf-with-none.pdf',False)]:
        with open(resource_filename('tests', 'data/%s' % fn), 'rb') as f:
            img = extract_first_jpeg_in_pdf(f)
            assert (len(img) == 5805) if has_image else (img is None)