.. _responses:

Responses
=========

.. module:: upyun.response


Response
--------

.. autoclass:: ResponseBase
   :members:
   :undoc-members:
   :private-members:
.. autoclass:: Response
   :show-inheritance:
.. autoclass:: PutImageResponse
   :show-inheritance:
.. autoclass:: InfoResponse
   :show-inheritance:
.. autoclass:: UsageResponse
   :show-inheritance:
.. autoclass:: GetResponse
   :show-inheritance:
.. autoclass:: LsResponse
   :show-inheritance:


Mixin
-----

.. autoclass:: ImageInfoMixin
   :members:
.. autoclass:: FileInfoMixin
   :members:
.. autoclass:: UsageMixin
   :members:
.. autoclass:: FileTypeMixin
   :members:
.. autoclass:: GetMixin
   :members:
.. autoclass:: LsMixin
   :members: files, folders, stuffs

   .. attribute:: File

      A namedtuple reprenting the file info

      `Fields`:

         ``name``
            File name

         ``path``
            File path

         ``url``
            File URL

         ``type``
            :const:`~upyun.const.FILE_TYPE_FILE`

         ``size``
            File size

         ``mtimt``
            Last modified time

   .. attribute:: Folder

      A namedtuple reprenting the folder info

      `Fields`:

         ``name``
            Folder name

         ``path``
            Folder path

         ``url``
            Folder URL

         ``type``
            :const:`~upyun.const.FILE_TYPE_FOLDER`

         ``size``
            Folder size

         ``mtimt``
            Last modified time
