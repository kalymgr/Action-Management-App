from actionmanagementapp.utilities.utility_classes import UploadHelper


def test_allowed_image_file():
    """
    testing the allowed image file method
    :return:
    """

    assert UploadHelper.allowed_image_file('test.jpg')
    assert UploadHelper.allowed_image_file('test.jpeg')
    assert UploadHelper.allowed_image_file('test.png')
    assert UploadHelper.allowed_image_file('test.gif')
    assert not UploadHelper.allowed_image_file('test.docx')
    assert not UploadHelper.allowed_image_file('testjpg')
