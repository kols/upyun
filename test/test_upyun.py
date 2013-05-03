import os.path
import unittest
from urllib import pathname2url

from upyun import const, UpYun


class UpYunTestCase(unittest.TestCase):
    #: File type bucket
    BUCKET_FILE = ''

    #: Image type bucket
    BUCKET_IMAGE = ''

    #: Username
    USERNAME = ''

    #: Password
    PASSWD = ''

    #: Predefined thumbnail version
    THUMB_VERSION = ''

    ASSET = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'asset')
    LOCAL_PATH_TXT_FILE = os.path.join(ASSET, 'upyun-test.txt')
    LOCAL_PATH_IMG_FILE = os.path.join(ASSET, 'upyun-test.gif')
    REMOTE_DIR = '/tmp/upyun-test'
    REMOTE_PATH_TXT_FILE = pathname2url(
            os.path.join(REMOTE_DIR, 'upyun-test.txt'))
    REMOTE_PATH_IMG_FILE = pathname2url(
            os.path.join(REMOTE_DIR, 'upyun-test.gif'))

    def setUp(self):
        self.client_file = UpYun(self.BUCKET_FILE, const.SPACE_TYPE_FILE,
                const.API_HOST_AUTO, (self.USERNAME, self.PASSWD))
        self.client_image = UpYun(self.BUCKET_IMAGE, const.SPACE_TYPE_IMAGE,
                const.API_HOST_AUTO, (self.USERNAME, self.PASSWD))
        self.test_file_txt = open(self.LOCAL_PATH_TXT_FILE)
        self.test_file_img = open(self.LOCAL_PATH_IMG_FILE, 'rb')

    def tearDown(self):
        self.test_file_txt.close()
        self.test_file_img.close()

    def _put_file(self):
        return self.client_file.put(
                self.REMOTE_PATH_TXT_FILE, self.test_file_txt)

    def _put_image(self, client=None):
        client = client or self.client_image
        return client.put(self.REMOTE_PATH_IMG_FILE, self.test_file_img)

    def test_put_file_space_file(self):
        resp = self._put_file()
        self.assertTrue(resp.success)

    def test_put_file_space_image(self):
        resp = self._put_image(self.client_file)
        self.assertTrue(resp.success)

    def test_put_image_space_image(self):
        resp = self._put_image(self.client_image)
        self.assertTrue(resp.success)

    def test_put_thumbnail_version(self):
        resp = self.client_image.put_thumbnail(self.REMOTE_PATH_IMG_FILE,
                self.test_file_img, self.THUMB_VERSION)
        self.assertTrue(resp.success)

    def test_put_thumbnail_version_modified(self):
        resp = self.client_image.put_thumbnail(self.REMOTE_PATH_IMG_FILE,
                self.test_file_img, self.THUMB_VERSION,
                const.THUMB_TYPE_FIX_MAX, (10,), 100, True)
        self.assertTrue(resp.success)

    def test_put_thumbnail_custom(self):
        resp = self.client_image.put_thumbnail(self.REMOTE_PATH_IMG_FILE,
                self.test_file_img, ttype=const.THUMB_TYPE_FIX_MAX, res=(10,),
                quality=100, sharpen=True)
        self.assertTrue(resp.success)

    def test_get_text_file(self):
        self._put_file()
        resp = self.client_file.get(self.REMOTE_PATH_TXT_FILE)
        self.assertTrue(resp.success)
        self.test_file_txt.seek(0)
        self.assertEqual(resp.data, self.test_file_txt.read())

    def test_get_binary_file(self):
        self._put_image()
        resp = self.client_file.get(self.REMOTE_PATH_IMG_FILE)
        self.assertTrue(resp.success)
        self.test_file_img.seek(0)
        self.assertEqual(resp.data, self.test_file_img.read())

    def test_ls(self):
        client = self.client_file
        self._put_file()
        self._put_image(client)
        resp = client.ls(self.REMOTE_DIR)
        self.assertTrue(resp.success)
        remote_file_paths = map(lambda f: f.path, resp.files.itervalues())
        self.assertTrue(self.REMOTE_PATH_TXT_FILE in remote_file_paths)
        self.assertTrue(self.REMOTE_PATH_IMG_FILE in remote_file_paths)

if __name__ == '__main__':
    unittest.main()
