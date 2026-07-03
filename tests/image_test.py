'''
Test module for use with py.test.
Read more here: http://pytest.org/
'''
from unittest import mock
from passporteye.mrz import image as image_module
from passporteye.mrz.image import _square_footprint


def test_square_footprint_shape():
    """Regardless of which scikit-image code path is taken, the footprint
    must be a `size` x `size` array of ones, matching what BooneTransform
    expects from morphology.square()/morphology.footprint_rectangle()."""
    fp = _square_footprint(5)
    assert fp.shape == (5, 5)
    assert (fp == 1).all()


def test_square_footprint_prefers_footprint_rectangle_when_available():
    """scikit-image >= 0.25 exposes footprint_rectangle and deprecates
    square() (removal scheduled for 0.27), so it must be preferred
    whenever available."""
    fake_morphology = mock.Mock(spec=['footprint_rectangle', 'square'])
    fake_morphology.footprint_rectangle.return_value = 'fp_result'
    with mock.patch.object(image_module, 'morphology', fake_morphology):
        result = _square_footprint(5)
    fake_morphology.footprint_rectangle.assert_called_once_with((5, 5))
    fake_morphology.square.assert_not_called()
    assert result == 'fp_result'


def test_square_footprint_falls_back_on_old_skimage():
    """scikit-image < 0.25 has no footprint_rectangle at all, so this must
    fall back to square() to keep supporting the package's stated floor
    of scikit-image >= 0.19.0."""
    fake_morphology = mock.Mock(spec=['square'])  # no footprint_rectangle attr
    fake_morphology.square.return_value = 'square_result'
    with mock.patch.object(image_module, 'morphology', fake_morphology):
        result = _square_footprint(5)
    fake_morphology.square.assert_called_once_with(5)
    assert result == 'square_result'
