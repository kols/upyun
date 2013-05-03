import hashlib
import os.path
from urllib import pathname2url
from urlparse import urljoin

import requests

from . import const, response
from .auth import UpYunDigestAuthentication


class UpYun(object):
    """Feature complete UpYun REST client

    :param str bucket: Your bucket
    :param stype: The space type, see :ref:`const.rst`
    :param api_host: API host to use, see :ref:`const.rst`
    :param tuple auth: Username, passwd tuple
    :param str domain: Your custom domain
    :param ssl: Whether to use SSL, only a *stub* for now

    Usage::

        client = UpYun('test', const.SPACE_TYPE_FILE, const.API_HOST_AUTO, ('user', 'pass'))
        client.put('/test.txt', open('/tmp/test.txt'))
    """
    def __init__(self, bucket, stype, api_host, auth, domain=None, ssl=False):
        self.bucket = bucket
        self.stype = stype
        self.api_host = api_host
        proto = 'https://' if ssl else 'http://'
        self._base_url = proto + const.UPAIYUN_API_HOSTS[self.api_host]
        self.domain = domain or (const.BUCKET_DOMAIN % bucket)
        self._bucket_base_url = proto + self.domain

        #: The :class:`requests.Session` object to use for the API requests
        self.session = self._prepare_session(auth, ssl)

    @property
    def api_host(self):
        return self._api_host

    @api_host.setter
    def api_host(self, api_host):
        if api_host in const.UPAIYUN_API_HOSTS:
            self._api_host = api_host
        else:
            raise

    @property
    def stype(self):
        return self._stype

    @stype.setter
    def stype(self, stype):
        if stype in [const.SPACE_TYPE_FILE, const.SPACE_TYPE_IMAGE]:
            self._stype = stype
        else:
            raise

    def _prepare_session(self, auth, ssl):
        if not ssl:
            self._auth = UpYunDigestAuthentication(*auth)
        s = requests.Session()
        s.auth = self._auth
        return s

    def _get_file_url(self, path):
        return urljoin(self._bucket_base_url, path)

    def _get_url(self, path):
        return urljoin(self._base_url,
                pathname2url(os.path.join(self.bucket, path.lstrip('/'))))

    def _get_data(self, fileo):
        try:
            data = fileo.read()
        except AttributeError:
            data = fileo
        return data

    def _digest(self, data):
        return hashlib.md5(data).hexdigest()

    def _prepare_put_request(self, path, fileo, mkdir, mimetype, secret,
            verify, headers=None):
        """Prepaer the put request"""
        url = self._get_url(path)
        data = self._get_data(fileo)
        headers = headers or {}
        req_headers = {}

        if mkdir:
            req_headers[const.HEADER_MKDIR] = 'true'
        if verify:
            req_headers[const.HEADER_MD5] = self._digest(data)
        if mimetype:
            req_headers['Content-Type'] = mimetype
        if secret:
            req_headers[const.HEADER_SECRET] = secret

        req_headers.update(headers)
        return url, data, req_headers

    def put(self, path, fileo, mkdir=True, mimetype=None, secret=None,
            verify=True, headers=None):
        """Put an file onto the server

        :param path: File path on the server
        :param fileo: File like object of the file to upload
        :param mkdir: Whether to make the parent folder if not existed
        :param mimetype: Mime-type of the file, used by server to determine
                         the extension of the file
        :param secret: Secret for user to later access the file uploaded
        :param verify: Whether to verify the file integrity using md5 hashing
        :param headers: Additional headers
        :return: :class:`~response.UploadedImageResponse`
        """
        url, data, headers = self._prepare_put_request(path, fileo, mkdir,
                mimetype, secret, verify, headers or {})
        resp = self.session.put(url=url, data=data, headers=headers)
        return response.UploadedImageResponse(resp, self._get_file_url(path))

    def put_thumbnail(self, path, fileo, version=None, ttype=None, res=None,
            quality=None, sharpen=None, **kwargs):
        """Put an image as a thumbnail on the server, the original image
        will not be uploaded

        :param path: Thumbnail path on the server
        :param fileo: File like object of the image
        :param version: Predefined thumbnail version name
        :param ttype: Thumbnail type, see :const:`~const.THUMB_TYPES`
        :param res: Image resolution, format: (width, height)
        :param quality: Image quality, default: 90
        :param sharpen: Whether to sharpen the image
        :type res: tuple
        :type sharpen: bool
        :return: :class:`~response.UploadedImageResponse`
        """
        if not (version or (ttype and res)):
            raise Exception(
                    'put: needs either version or thumbnail type, or both')
        headers = {}
        if version:
            if self.stype != const.SPACE_TYPE_IMAGE:
                raise Exception('put: need space type image')
            headers[const.HEADER_THUMB_VERSION] = version
        if ttype:
            if ttype not in const.THUMB_TYPES:
                raise Exception('put: invalid thumbnail type')
            headers[const.HEADER_THUMB_TYPE] = const.THUMB_TYPES[ttype]
            if res:
                if ttype in (const.THUMB_TYPE_FIX_BOTH,
                        const.THUMB_TYPE_FIX_WIDTH_OR_HEIGHT):
                    res_val = res[0] + 'x' + res[1]
                else:
                    res_val = res[0]
                headers[const.HEADER_THUMB_VALUE] = res_val
        if quality:
            headers[const.HEADER_THUMB_QUALITY] = int(quality)
        if sharpen is not None:
            headers[const.HEADER_THUMB_UNSHARP] = str(not sharpen).lower()

        uheaders = kwargs.pop('headers', {})
        headers.update(uheaders)

        return self.put(path, fileo, headers=headers, **kwargs)

    def get(self, path):
        """Get a file

        :param path: Path of the file to retrieve
        :return: :class:`~response.GetResponse`
        """
        resp = self.session.get(self._get_url(path))
        return response.GetResponse(resp, self._get_file_url(path))

    def delete(self, path):
        """Delete a file or an empty folder

        :param path: Path of the file or folder to delete
        :return: :class:`~response.Response`
        """
        resp = self.session.delete(self._get_url(path))
        return response.Response(resp, None)

    def mkdir(self, dirname, mk_parent=True):
        """Create a folder on server

        :param dirname: Folder name
        :param mk_parent: Whether to create the parent folder if not existed
        :return: :class:`~response.Response`
        """
        url = self._get_url(dirname)
        headers = {}
        headers[const.HEADER_FOLDER] = 'create'
        if mk_parent:
            headers[const.HEADER_MKDIR] = 'true'
        resp = self.session.post(url, headers=headers)
        return response.Response(resp, self._get_file_url(dirname))

    def ls(self, path):
        resp = self.session.get(self._get_url(path))
        return response.LsResponse(resp, self._get_file_url(path))

    def usage(self):
        """Retrieve the space usage info

        :return: :class:`~response.UsageResponse`
        """
        resp = self.session.get(self._get_url('?usage'))
        return response.UsageResponse(resp, None)

    def info(self, path):
        """Retrieve file info

        :return: :class:`~response.FileInfoResponse`
        """
        resp = self.session.head(self._get_url(path))
        return response.FileInfoResponse(resp, self._get_file_url(path))
