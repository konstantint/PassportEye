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
