from collections import namedtuple
import copy
import os.path
import urllib
import urlparse
from datetime import datetime

import requests

from upyun import const


class ResponseBase(object):
    """A response of successfully uploading image, contains extra info
    of the uploaded image

    :param response: Response from UpYun
    :type response: :class:`requests.Response`
    :param str url: URL of the file on the UpYun
    """
    def __init__(self, response, url):
        #: Response from UpYun
        self.response = response

        #: URL of the file on the UpYun
        self.url = url

        #: Whether the API request is successful
        self.success = self.response.status_code == requests.codes.ok

    def _get_header_with_prefix(self, name):
        return self.response.headers.get(const.UPYUN_HEADER_PREFIX + name)


class UploadedImageInfoMixin(object):
    @property
    def width(self):
        """
        Width of the image

        :rtype: int or None
        """
        w = self._get_header_with_prefix('width')
        return int(w) if w else None

    @property
    def height(self):
        """
        Height of the image

        :rtype: int or None
        """
        h = self._get_header_with_prefix('height')
        return int(h) if h else None

    @property
    def frames(self):
        """
        Frames of the image

        :rtype: int or None
        """
        f = self._get_header_with_prefix('frames')
        return int(f) if f else None


class FileInfoMixin(object):
    @property
    def date(self):
        """File created date

        :rtype: datetime.datetime
        """
        return self._get_header_with_prefix('date')

    @property
    def size(self):
        """File size

        :rtype: int or None
        """
        s = self._get_header_with_prefix('size')
        return int(s) if s else None


class UsageMixin(object):
    @property
    def usage(self):
        """Usage of the space in bytes

        :rtype: int
        """
        return int(self.response.text)


class FileTypeMixin(object):
    @property
    def type(self):
        """File type of the queried path

        :return: one of ['file', 'folder']
        """
        return self._get_header_with_prefix('type')


class GetMixin(object):
    @property
    def data(self):
        """Data of the downloaded file

        :rtype: file
        """
        return self.response.content


class LsMixin(object):
    TYPE_FILE = 'N'
    TYPE_FOLDER = 'F'

    _fields = ['name', 'path', 'url', 'type', 'size', 'mtime']
    File = namedtuple('File', _fields)
    Folder = namedtuple('Folder', _fields)

    def _parse_content(self):
        self._files = {}
        self._folders = {}

        for l in self.response.content.strip().split("\n"):
            name, type, size, mtime = l.strip().split()

            type = type.upper()
            url_parsed = urlparse.urlparse(self.url)
            folder_path = url_parsed.path

            path = urllib.pathname2url(os.path.join(folder_path, name))
            url = urlparse.urljoin(
                    (url_parsed.scheme + '://' + url_parsed.netloc), path)
            mtime = datetime.utcfromtimestamp(int(mtime))

            if type == self.TYPE_FILE:
                f = self.File(name=name, path=path, url=url,
                        type=const.FILE_TYPE_FILE, size=int(size), mtime=mtime)
                self._files[name] = f
            elif type == self.TYPE_FOLDER:
                f = self.File(name=name, path=path, url=url,
                        type=const.FILE_TYPE_FILE, size=int(size), mtime=mtime)
                self._folders[name] = f

    @property
    def files(self):
        if not hasattr(self, '_files'):
            self._parse_content()
        return self._files

    @property
    def folders(self):
        if not hasattr(self, '_folders'):
            self._parse_content()
        return self._folders

    @property
    def stuff(self):
        stuff = copy.deepcopy(self.files)
        stuff.update(self.folders)
        return stuff


class UploadedImageResponse(ResponseBase, UploadedImageInfoMixin,
        FileTypeMixin):
    pass


class FileInfoResponse(ResponseBase, FileInfoMixin, FileTypeMixin):
    pass


class UsageResponse(ResponseBase, UsageMixin):
    pass


class GetResponse(ResponseBase, GetMixin):
    pass


class LsResponse(ResponseBase, LsMixin):
    pass


class Response(ResponseBase):
    pass
