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

The :py:class:`khoros.Khoros` object can be initiated in two different ways:

* Passing the information directly into the object
* Leveraging a "helper" configuration file

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
