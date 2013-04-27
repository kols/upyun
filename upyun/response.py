import requests

from upyun import const


class ResponseBase(object):
    """A response of successfully uploading image, contains extra info
    of the uploaded image

    :ivar response: Response from UpYun
    :type response: :class:`requests.Response`
    :ivar url: URL of the file on the UpYun
    """
    def __init__(self, response, url):
        """
        :param response: Response from UpYun
        :type response: :class:`requests.Response`
        :param string url: URL of the file on the UpYun
        """
        self.response = response
        self.url = url

    def _get_header_with_prefix(self, name):
        return self.response.headers.get(const.UPYUN_HEADER_PREFIX + name)

    @property
    def success(self):
        """
        Whether the request is successful

        :rtype: bool
        """
        return self.response.status_code == requests.codes.ok


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


class UploadedImageResponse(ResponseBase, UploadedImageInfoMixin,
        FileTypeMixin):
    pass


class FileInfoResponse(ResponseBase, FileInfoMixin, FileTypeMixin):
    pass


class UsageResponse(ResponseBase, UsageMixin):
    pass


class GetResponse(ResponseBase, GetMixin):
    pass


class Response(ResponseBase):
    pass
