############
Introduction
############
The  **khoros**  library acts as a Python software development kit (SDK) to administer and manage
`Khoros Community <https://developer.khoros.com/khoroscommunitydevdocs>`_ (formerly Lithium) online
community platforms.

* `Installation`_
* `Change Log`_
* `Usage`_
    * `Importing the Package`_
    * `Initializing a Khoros object instance`_
        * `Passing the information directly into the object`_
        * `Leveraging a "helper" configuration file`_
    * `Interacting with the Community APIs`_
* `License`_
* `Reporting Issues`_
* `Disclaimer`_

************
Installation
************
The package can be installed via pip using the syntax below.

.. code-block:: shell

   pip install khoros

You may also clone the repository and install from source using below.

.. code-block:: shell

   git clone git://github.com/jeffshurtliff/khoros.git
   cd khoros/
   python3 setup.py install

:doc:`Return to Top <introduction>`

|

**********
Change Log
**********
Changes for each release can be found on the :doc:`Change Log <changelog>` page.

:doc:`Return to Top <introduction>`

|

*****
Usage
*****
This section provides basic usage instructions for the package.

:doc:`Return to Top <introduction>`

|

Importing the Package
=====================
Rather than importing the base package, it is recommended that you import the primary :py:class:`khoros.Khoros`
class using the syntax below.

.. code-block:: python

   from khoros import Khoros

This recommendation is because the best practice is to use the name ``khoros`` when naming your object instance.

:doc:`Return to Top <introduction>`

|

Initializing a Khoros object instance
=====================================
The primary :py:class:`khoros.Khoros` object serves many purposes, the most important being to establish a
connection to the Khoros Community environment with which you intend to interact. As such, when initializing an
instance of the :py:class:`khoros.Khoros` object, you will need to pass it the community URL, the credentials
it will use and related information so that the connection can be established.

The :py:class:`khoros.Khoros` object can be initiated in three different ways:

* `Passing the information directly into the object`_
* `Leveraging a "helper" configuration file`_
* `Utilizing environment variables`_

:doc:`Return to Top <introduction>`

|

Passing the information directly into the object
------------------------------------------------
The community and connection information can be passed directly into the :py:class:`khoros.Khoros` object when
initializing it, as demonstrated in the example below.

.. code-block:: python

   khoros = Khoros(
       community_url='https://community.example.com',
       session_auth={'username': USERNAME, 'password': PASSWD}
   )

Alternatively, configuration settings can be passed at once using the ``options`` argument in the
:py:class:`khoros.Khoros` class, as shown below.

.. code-block:: python

   my_settings = {
       'community_url': 'https://community.example.com',
       'community_name': 'mycommunity',
       'auth_type': 'session_auth',
       'session_auth': {
           'username': USERNAME,
           'password': PASSWD
       }
   }

:doc:`Return to Top <introduction>`

|

Leveraging a "helper" configuration file
----------------------------------------
As an alternative to passing the connection information to the :py:class:`khoros.Khoros` class in the ways
demonstrated above, a "helper" configuration file in `yaml <https://en.wikipedia.org/wiki/YAML>`_ or
`json <https://en.wikipedia.org/wiki/JSON>`_ format can be leveraged instead and passed to the
:py:class:`khoros.Khoros` class when initializing the object.

This is an example of how the configuration file would be written:

.. code-block:: yaml

   # Helper configuration file for the khoros package

   # Define how to obtain the connection information
   connection:
       community_url: https://community.example.com/
       tenant_id: example12345

       # Define the default authentication type to use
       default_auth_type: session_auth

       # Define the OAuth 2.0 credentials
       oauth2:
           client_id: FLFeNYob7XXXXXXXXXXXXXXXXXXXXZcWQEQHR5T6bo=
           client_secret: 1n0AIXXXXXXXXXXXXXXXXXXXX1udOtNaYnfJCeOszYw=
           redirect_url: http://redirect.community.example.com/getAccessToken

       # Define the session key authorization information
       session_auth:
           username: serviceaccount
           password: Ch@ng3ME!

   # Define the preferred format for API responses
   prefer_json: yes

The file can then be referenced using the ``helper`` argument when initializing the object instance, as shown below.

.. code-block:: python

   HELPER_FILE = "/path/to/helper.yml"
   khoros = Khoros(helper=HELPER_FILE)

:doc:`Return to Top <introduction>`

|

Utilizing environment variables
-------------------------------
This third method of initializing a Khoros object instance is definitely the easiest, as it allows you to call
upon the :py:class:`khoros.Khoros` class without passing any arguments, as shown below.

.. code-block:: python

   from khoros import Khoros
   khoros = Khoros()

This is accomplished by defining environment variables within your Operating System, either through the
`graphical UI <https://www.techjunkie.com/environment-variables-windows-10/>`_, the command-line or within the Python
IDE using the :py:mod:`os` module and
`adding entries <https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5>`_ to the
``os.environ`` dictionary, as shown below.

.. code-block:: python

   import os
   os.environ['KHOROS_URL'] = 'https://community.example.com'

The environment variables leveraged in the :py:mod:`khoros` library are listed below.

.. list-table:: Khoros Environment Variables
   :widths: 30 35 35
   :header-rows: 1

   * - Environment Variable
     - Description
     - Example
   * - KHOROS_URL
     - The base URL of the environment
     - ``https://community.example.com``
   * - KHOROS_TENANT_ID
     - The `Tenant ID <https://developer.khoros.com/khoroscommunitydevdocs/docs/oauth-authorization-grant>`_
       associated with your environment
     - ``abcde12345``
   * - KHOROS_DEFAULT_AUTH
     - The default authentication method you wish to use
     - ``session_auth``
   * - KHOROS_OAUTH_ID
     - The Client ID utilized by the
       `OAuth 2.0 <https://developer.khoros.com/khoroscommunitydevdocs/docs/oauth-authorization-grant>`_
       authorization grant flow
     - ``FXXXXXXb7owXXXXXXo+jFlPXXXXXXjZcWQXXXXXX6bo=``
   * - KHOROS_OAUTH_SECRET
     - The Client Secret utilized by the
       `OAuth 2.0 <https://developer.khoros.com/khoroscommunitydevdocs/docs/oauth-authorization-grant>`_
       authorization grant flow
     - ``1XXXXXX+/kZXXXXXXZZ9u1B5+1uXXXXXXfJCeOszYw=``
   * - KHOROS_OAUTH_REDIRECT_URL
     - The Redirect URL utilized by the
       `OAuth 2.0 <https://developer.khoros.com/khoroscommunitydevdocs/docs/oauth-authorization-grant>`_
       authorization grant flow
     - ``http://redirect.community.example.com/getAccessToken``
   * - KHOROS_SESSION_USER
     - The username to use with `Session Key <https://developer.khoros.com/khoroscommunitydevdocs/docs/session-key>`_
       authentication
     - ``apiuser``
   * - KHOROS_SESSION_PW
     - The password to use with `Session Key <https://developer.khoros.com/khoroscommunitydevdocs/docs/session-key>`_
       authentication
     - ``Ch@ng3M3!``
   * - KHOROS_PREFER_JSON
     - Boolean string indicating if JSON responses are preferred
     - ``True``
   * - KHOROS_LIQL_PRETTY
     - Boolean string indicating if reader-friendly formatting should be used
     - ``False``
   * - KHOROS_LIQL_TRACK_LSI
     - Boolean string indicating if queries should be captured in Community Analytics search reports
     - ``False``
   * - KHOROS_LIQL_ALWAYS_OK
     - Boolean string indicating if all responses should return a ``200 OK`` status code
     - ``False``

If you are leveraging this library on a macOS or Linux operating system (e.g. Ubuntu Server) then you can simply
add the environment variables you wish to define to either the ``/etc/environment`` file if you wish to apply
them to all users, or to your user's ``~/.bashrc`` file for them to only apply to your user.

.. code-block:: bash

   # Define environment variables for Khoros
   KHOROS_URL='https://community.example.com'

.. note:: You will generally need to log out and log back in for the changes to take effect.

If you are leveraging this library on a Windows operating system (e.g. Windows 10) then you can add environment
variables for your user via the Command Prompt (i.e. ``cmd.exe``) or  PowerShell.

.. note:: Using either of these two methods, you can add the environment variables using an interactive terminal
          window or using a batch/script file.  (Files should use the ``.bat`` or ``.cmd`` extension for the
          Command Prompt and ``.ps1`` for PowerShell.)

**Command Prompt**

.. code-block:: bat

   @echo off
   echo Defining the KHOROS_URL environment variable...
   setx KHOROS_URL https://community.example.com
   echo.

**PowerShell**

.. code-block:: powershell

   "Defining the KHOROS_URL environment variable..."
   [Environment]::SetEnvironmentVariable("KHOROS_URL", "https://community.example.com/", "User")

:doc:`Return to Top <introduction>`

|

Interacting with the Community APIs
===================================
Once the :py:class:`khoros.Khoros` object instance has been initialized, it can be leveraged to interact
with a Khoros Community environment in many ways, which will be fully documented shortly in the
`documentation <https://khoros.readthedocs.io/en/latest/>`_. The example below demonstrates how
a search can be performed using LiQL to return information from the environment in
`json <https://en.wikipedia.org/wiki/JSON>`_ format.

.. code-block:: python

   response_json = khoros.search(
       select_fields=('id', 'view_href'),
       from_source='messages',
       where_filter=('style', 'tkb'),
       order_by='last_post_time',
       limit=5
   )

:doc:`Return to Top <introduction>`

|

*******
License
*******
This package falls under the `MIT License <https://github.com/jeffshurtliff/khoros/blob/master/LICENSE>`_.

:doc:`Return to Top <introduction>`

|

****************
Reporting Issues
****************
Issues can be reported within the `GitHub repository <https://github.com/jeffshurtliff/khoros/issues>`_.

:doc:`Return to Top <introduction>`

|

**********
Disclaimer
**********
This package is considered unofficial and is in no way endorsed or supported by `Khoros, LLC <https://www.khoros.com>`_.

:doc:`Return to Top <introduction>`
