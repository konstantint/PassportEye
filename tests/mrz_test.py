'''
Test module for use with py.test.
Write each test as a function named test_<something>.
Read more here: http://pytest.org/

Author: Peter Horsley
License: MIT
'''
import io
from passporteye import read_mrz

def read_img(filename, as_stream=False):
    file = io.open(filename, "rb", buffering=0) if as_stream else filename
    return read_mrz(file, extra_cmdline_params='--oem 0')

def test_td2_td3_stream_nonstream():
    for fn, test_fn in [('./tests/data/passport-td3.jpg', assert_td3_jpg),
                        ('./tests/data/passport-td3.png', assert_td3_png),
                        ('./tests/data/passport-td2.jpg', assert_td2_jpg),
                        ('./tests/data/passport-td2.png', assert_td2_png),
                       ]:
        for as_stream in [True, False]:
            test_fn(read_img(fn, as_stream=as_stream))

def assert_td3_jpg(mrz):
    assert mrz is not None
    assert mrz.mrz_type == 'TD3'
    assert mrz.valid_score >= 62  # Can be 100 on some Tesseract installations
    assert mrz.type == 'P<'
    assert mrz.country == 'UTO'
    assert mrz.number == 'L898902C3'
    assert mrz.date_of_birth == '740812'
    assert mrz.expiration_date == '120415'
    assert mrz.nationality == 'UTO'
    assert mrz.sex == 'F'
    assert mrz.names == 'ANNA MARIA'
    assert mrz.surname == 'ERIKSSON'
    assert mrz.personal_number in ['2E184226B<<<<<', 'ZE184226B<<<<<']
    assert mrz.check_number == '6'
    assert mrz.check_date_of_birth == '2'
    assert mrz.check_expiration_date == '9'
    assert mrz.check_composite == '0'
    assert mrz.check_personal_number == '1'
    assert mrz.valid_number
    assert mrz.valid_date_of_birth
    assert mrz.valid_expiration_date

def assert_td3_png(mrz):
    assert mrz is not None
    assert mrz.mrz_type == 'TD3'
    assert mrz.valid_score == 100
    assert mrz.type == 'P<'
    assert mrz.country == 'UTO'
    assert mrz.number == 'L898902C3'
    assert mrz.date_of_birth == '740812'
    assert mrz.expiration_date == '120415'
    assert mrz.nationality == 'UTO'
    assert mrz.sex == 'F'
    assert mrz.names == 'ANNA MARIA'
    assert mrz.surname == 'ERIKSSON'
    assert mrz.personal_number in ['2E184226B<<<<<', 'ZE184226B<<<<<']
    assert mrz.check_number == '6'
    assert mrz.check_date_of_birth == '2'
    assert mrz.check_expiration_date == '9'
    assert mrz.check_composite == '0'
    assert mrz.check_personal_number == '1'
    assert mrz.valid_number
    assert mrz.valid_date_of_birth
    assert mrz.valid_expiration_date

def assert_td2_jpg(mrz):
    assert mrz.mrz_type == 'TD2'
    assert mrz.valid_score == 100
    assert mrz.type == 'I<'
    assert mrz.country == 'UTO'
    assert mrz.number == 'D23145890'
    assert mrz.date_of_birth == '740812'
    assert mrz.expiration_date == '120415'
    assert mrz.nationality == 'UTO'
    assert mrz.sex == 'F'
    assert mrz.names == 'ANNA MARIA'
    assert mrz.surname == 'ERIKSSON'
    assert mrz.optional1 == '<<<<<<<'
    assert mrz.check_number == '7'
    assert mrz.check_date_of_birth == '2'
    assert mrz.check_expiration_date == '9'
    assert mrz.check_composite == '6'
    assert mrz.valid_number
    assert mrz.valid_date_of_birth
    assert mrz.valid_expiration_date
    assert mrz.valid_composite

def assert_td2_png(mrz):
    assert mrz.mrz_type == 'TD2'
    assert mrz.valid_score == 100
    assert mrz.type == 'I<'
    assert mrz.country == 'UTO'
    assert mrz.number == 'D23145890'
    assert mrz.date_of_birth == '740812'
    assert mrz.expiration_date == '120415'
    assert mrz.nationality == 'UTO'
    assert mrz.sex == 'F'
    assert mrz.names == 'ANNA MARIA'
    assert mrz.surname == 'ERIKSSON'
    assert mrz.optional1 == '<<<<<<<'
    assert mrz.check_number == '7'
    assert mrz.check_date_of_birth == '2'
    assert mrz.check_expiration_date == '9'
    assert mrz.check_composite == '6'
    assert mrz.valid_number
    assert mrz.valid_date_of_birth
    assert mrz.valid_expiration_date
    assert mrz.valid_composite


def test_issue55_method_always_set(monkeypatch):
    # OCR output without any '<' (e.g. all fillers misread as 'X') still parses with a positive score.
    # BoxToMRZ used to return such an MRZ without aux['method'], making TryOtherMaxWidth fail with KeyError.
    import numpy as np
    import passporteye.mrz.image as image
    text = ('PXUTOERIKSSONXXANNAXMARIAXXXXXXXXXXXXXXXXXXX\n'
            'L898902C36UTO7408122F1204159ZE184226BXXXXX10')
    monkeypatch.setattr(image, 'ocr', lambda *args, **kwargs: text)
    box = image.RotatedBox([50, 50], 80, 20, 0)
    roi, ocr_text, mrz = image.BoxToMRZ()(box, np.ones((100, 100)), np.ones((100, 100)), 1.0)
    assert mrz.valid_score > 0
    assert mrz.aux['method'] == 'direct'

    class FakePipeline(dict):
        def replace_component(self, name, component):
            pass
    pipeline = FakePipeline(img_binary=np.zeros((2, 2)), img=np.ones((2, 2)), mrz=mrz)
    result = image.TryOtherMaxWidth()(None, pipeline)
    assert result.aux['method'] == 'direct|max_width(1000)'


def test_issue38_input_types():
    # The image may also be given as a pixel array (e.g. an OpenCV frame), a PIL Image, an encoded buffer or a Path
    import pathlib
    import numpy as np
    import imageio.v3 as iio
    from PIL import Image
    fn = './tests/data/passport-td2.png'
    raw = open(fn, 'rb').read()
    pixels = iio.imread(fn)
    pixels_copy = pixels.copy()
    for file in [pixels, Image.open(fn), np.frombuffer(raw, np.uint8).reshape(-1, 1),  # cv2.imencode output shape
                 bytearray(raw), memoryview(raw), pathlib.Path(fn)]:
        assert_td2_png(read_mrz(file, extra_cmdline_params='--oem 0'))
    assert np.array_equal(pixels, pixels_copy)  # The caller's array is not modified


def test_no_image():
    import pytest
    assert read_mrz('./tests/data/pdf-with-none.pdf') is None
    with pytest.raises(TypeError):
        read_mrz(12345)
