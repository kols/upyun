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

   .. autoattribute:: files
   .. autoattribute:: folders
   .. autoattribute:: stuffs
   .. class:: upyun.response.LsMixin.File

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

   .. class:: upyun.response.LsMixin.Folder

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
