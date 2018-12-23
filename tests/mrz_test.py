'''
Test module for use with py.test.
Write each test as a function named test_<something>.
Read more here: http://pytest.org/

Author: Peter Horsley
License: MIT
'''
import io
from passporteye import read_mrz

def test_read_mrz_td3_jpg_file():
    mrz = read_mrz('./tests/data/passport-td3.jpg')
    assert_td3_jpg(mrz)

def test_read_mrz_td3_jpg_stream():
    byteStream = None
    mrz = None
    try:
        byteStream = io.open('./tests/data/passport-td3.jpg', "rb", buffering=0)
        mrz = read_mrz(byteStream)
    finally:
        if byteStream is not None:
            byteStream.close()
    assert_td3_jpg(mrz)

def test_read_mrz_td3_png_file():
    mrz = read_mrz('./tests/data/passport-td3.png')
    assert_td3_png(mrz)

def test_read_mrz_td3_png_stream():
    byteStream = None
    mrz = None
    try:
        byteStream = io.open('./tests/data/passport-td3.png', "rb", buffering=0)
        mrz = read_mrz(byteStream)
    finally:
        if byteStream is not None:
            byteStream.close()
    assert_td3_png(mrz)

def test_read_mrz_td2_jpg_file():
    mrz = read_mrz('./tests/data/passport-td2.jpg')
    assert_td2_jpg(mrz)

def test_read_mrz_td2_jpg_stream():
    byteStream = None
    mrz = None
    try:
        byteStream = io.open('./tests/data/passport-td2.jpg', "rb", buffering=0)
        mrz = read_mrz(byteStream)
    finally:
        if byteStream is not None:
            byteStream.close()
    assert_td2_jpg(mrz)

def test_read_mrz_td2_png_file():
    mrz = read_mrz('./tests/data/passport-td2.png')
    assert_td2_png(mrz)

def test_read_mrz_td2_png_stream():
    byteStream = None
    mrz = None
    try:
        byteStream = io.open('./tests/data/passport-td2.png', "rb", buffering=0)
        mrz = read_mrz(byteStream)
    finally:
        if byteStream is not None:
            byteStream.close()
    assert_td2_png(mrz)

def assert_td3_jpg(mrz):
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
    assert mrz.valid_number == True
    assert mrz.valid_date_of_birth == True
    assert mrz.valid_expiration_date == True
    #assert mrz.valid_composite == False
    #assert mrz.valid_personal_number == False

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
    assert mrz.valid_number == True
    assert mrz.valid_date_of_birth == True
    assert mrz.valid_expiration_date == True
    #assert mrz.valid_composite == True
    #assert mrz.valid_personal_number == True

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
    assert mrz.valid_number == True
    assert mrz.valid_date_of_birth == True
    assert mrz.valid_expiration_date == True
    assert mrz.valid_composite == True

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
    assert mrz.valid_number == True
    assert mrz.valid_date_of_birth == True
    assert mrz.valid_expiration_date == True
    assert mrz.valid_composite == True
