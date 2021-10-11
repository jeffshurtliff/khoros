######################
Managing Node Settings
######################
You can manage the settings on any node (including categories, boards and grouphubs)
using the :py:class:`khoros.core.Khoros.Settings` subclass, which leverages the
:py:mod:`khoros.objects.settings` module.

This guide demonstrates various ways that you can retrieve, define and update the
node settings within your Khoros Communities environment.

* `Prerequisites`_
* `Retrieving node settings`_
    * `Retrieving board settings`_
    * `Retrieving category settings`_
    * `Retrieving group hub settings`_
* `Defining node settings`_
* `Working with JSON strings`_
* `Troubleshooting`_
    * `An unexpected error has occurred when defining a node setting`_
    * `Unable to define node settings using the API v2 field name`_
    * `No board with the specified dispid error`_

*************
Prerequisites
*************
Throughout this guide we will assume that the Khoros core object has already been
instantiated as ``khoros`` as shown below.

.. code-block:: python

   >>> from khoros import Khoros
   >>> khoros = Khoros(helper='/Users/example/helper.yml')

|

************************
Retrieving node settings
************************
This section demonstrates how easy it is to retrieve a specific setting value from a node.

.. caution::
   These methods and functions assume you are querying a **board** by default.
   An additional parameter must be passed in order to query a **category** or
   **grouphub** node, as will be explained.

|

Retrieving board settings
=========================
A specific setting for a board can be retrieved using the
:py:meth:`khoros.core.Khoros.Settings.get_node_setting` method, which leverages the
underlying :py:func:`khoros.objects.settings.get_node_setting` function.

In this method, the first parameter is the name of the setting to retrieve and the second
parameter is the Node ID for the node to be queried. Depending on the field name, the method (and
underlying function) will attempt to select the appropriate Community API for the job.

For example, because most--if not all--custom settings set up by Khoros within the v2 API begin with
the ``c_`` prefix (with the ``c`` implying *custom*), if a setting with the name ``c_primary_moderator``
was provided as the first parameter then the v2 API will automatically be selected and a LiQL query will
be utilized to retrieve the value.

Alternatively, as API v1 values are generally defined in `namespace <https://en.wikipedia.org/wiki/Namespace>`_
notation, a field with the name ``custom.primary_moderator`` would leverage the v1 API within the method/function
to retrieve the value.

.. code-block:: python

   >>> khoros.settings.get_node_setting('c_primary_moderator',
   ...                                  'product-blog')
   'cmmgr123'
   >>> khoros.settings.get_node_setting('custom.primary_moderator',
   ...                                  'product-blog')
   'cmmgr123'

However, if you want to ensure that the appropriate API version is leveraged then you can explicitly
define it using the ``v1`` parameter by defining it as either ``True`` or ``False``.

.. code-block:: python

   >>> khoros.settings.get_node_setting('c_primary_moderator',
   ...                                  'product-blog',
   ...                                  v1=False)
   'cmmgr123'
   >>> khoros.settings.get_node_setting('custom.primary_moderator',
   ...                                  'product-blog',
   ...                                  v1=True)
   'cmmgr123'

|

Retrieving category settings
============================
Retrieving a node setting from a category is nearly identical to retrieving board settings, with the
one caveat that you must explicitly define the node type in the third parameter, as illustrated below.

.. code-block:: python

   >>> khoros.settings.get_node_setting('c_primary_moderator',
   ...                                  'our-awesome-product',
   ...                                  'category')
   'cmmgr123'
   >>> khoros.settings.get_node_setting('custom.primary_moderator',
   ...                                  'our-awesome-product',
   ...                                  'category')
   'cmmgr123'

.. caution::

   It is important to note that the node type should be defined in **singular form** rather than in
   **plural**.  This means that ``category``, ``board`` and ``grouphub`` are the three acceptable values.

|

Retrieving group hub settings
=============================
Similar to retrieving category settings, you must explicitly define the node type using the ``grouphub`` value
to successfully retrieve the value, as demonstrated below.

.. code-block:: python

   >>> khoros.settings.get_node_setting('c_primary_moderator',
   ...                                  'api-users-group',
   ...                                  'grouphub')
   'cmmgr123'
   >>> khoros.settings.get_node_setting('custom.primary_moderator',
   ...                                  'api-users-group',
   ...                                  'grouphub')
   'mgr123'

|

**********************
Defining node settings
**********************
It is just as easy to define or update node settings with this library, which is done using the
:py:meth:`khoros.core.Khoros.Settings.define_node_setting` method and the underlying function
:py:func:`khoros.objects.settings.define_node_setting`.

The primary difference is that you will obviously need to specify the value of the metadata field
when invoking the method. This value will **always be a string** for custom metadata as this is
how said fields are always configured. As such, it is always a good idea to leverage
`literal string interpolation <https://www.python.org/dev/peps/pep-0498/>`_ when there is any
uncertainty about the data type.

With the :py:meth:`khoros.core.Khoros.Settings.define_node_setting` method, the first parameter is
the name of the custom field, the second parameter is the value to write to said field, the third
parameter is the Node ID of the affected node and the fourth parameter is the node type.

You will know your operation was successful when the standard success response is received as a JSON
string or object, as shown in the examples below.

.. code-block:: python

   >>> khoros.settings.define_node_setting('custom.primary_moderator',
   ...                                     'johnDoe',
   ...                                     'product-blog')
   '{"status": "success"}'
   >>> khoros.settings.define_node_setting('custom.primary_moderator',
   ...                                     'johnDoe',
   ...                                     'our-awesome-product',
   ...                                     'category')
   '{"status": "success"}'
   >>> khoros.settings.define_node_setting('custom.primary_moderator',
   ...                                     'johnDoe',
   ...                                     'api-users-group',
   ...                                     'grouphub')
   '{"status": "success"}'

|

*************************
Working with JSON strings
*************************
Utilizing JSON objects in custom metadata can add many opportunities for customization and
automation with your community. Rather than just storing a basic text string value in your
metadata, you could store multiple values by treating the string as a JSON object.

For example, instead of just tracking the username of the node's primary moderator as was
done in the examples above, you may wish to keep other relevant data in the same field. This
could be accomplished with a JSON object similar to the following:

.. code-block:: json

   {
     "primary_moderator": {
       "full_name": "John Doe",
       "login": "johnDoe",
       "email": "john.doe@example.com"
     }
   }

By converting the JSON object to a string, you can pass it as the metadata value as shown in
the example below.

.. code-block:: python

   >>> import json
   >>>
   >>> # Store the metadata
   >>> moderator_info = {
   ...     'primary_moderator': {
   ...         'full_name': 'John Doe',
   ...         'login': 'johnDoe',
   ...         'email': 'john.doe@example.com'
   ...     }
   ... }
   >>> khoros.settings.define_node_setting('custom.moderator_info',
   ...                                     json.dumps(moderator_info),
   ...                                     'product-blog')
   '{"status": "success"}'
   >>>
   >>> # Retrieve the metadata
   >>> data = khoros.settings.get_node_setting('custom.moderator_info',
   ...                                         'product-blog')
   >>> moderator_info = json.loads(data)
   >>> print(f'The primary moderator is ${moderator_info["primary_moderator"]["full_name"]}.')
   The primary moderator is John Doe.

You also have the option of using the ``convert_json`` Boolean parameter in the
:py:meth:`khoros.settings.get_node_setting` method to automatically convert the JSON string
to a Python dictionary to save yourself the step of converting it manually with the
:py:func:`json.loads` function.

.. code-block:: python

   >>> data = khoros.settings.get_node_setting('custom.moderator_info',
   ...                                         'product-blog',
   ...                                         convert_json=True)
   >>> print(f'The primary moderator is ${data["primary_moderator"]["full_name"]}.')
   The primary moderator is John Doe.

.. note:: A future release will introduce the ability to dump JSON to a string when defining node settings.

|

***************
Troubleshooting
***************
This section addresses some of the most commonly experienced issues when managing node settings.

An unexpected error has occurred when defining a node setting
=============================================================
Whenever an attempt is made to define a custom metadata field that does not exist, an
``Unexpected Error`` message will be returned, as shown below.

.. code-block:: python

   >>> khoros.settings.define_node_setting('custom.fake_field',
   ...                                     'John Doe',
   ...                                     'product-blog')
   {'status': 'error', 'error': {'code': 100, 'message': 'An Unexpected Error has occurred.'}}

Unable to define node settings using the API v2 field name
==========================================================
Community API v2 metadata field names are considered read-only and have the sole purpose of allowing
you to retrieve the data with a LiQL query. Therefore, it is by design that you are unable to write
to said field. Attempting to do so will likely return an ``Unexpected Error`` message, as shown below.

.. code-block:: python

   >>> khoros.settings.define_node_setting('c_primary_moderator',
   ...                                     'johnDoe',
   ...                                     'product-blog')
   {'status': 'error', 'error': {'code': 100, 'message': 'An Unexpected Error has occurred.'}}

No board with the specified dispid error
========================================
When a Node ID is not recognized in the Khoros Communities environment, the error message
``No board with the specified dispid`` will be returned in the API response, as shown below.

.. code-block:: python

   >>> khoros.settings.get_node_setting('custom.primary_moderator', 'api-users-group')
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/johndoe/Development/khoros/khoros/core.py", line 3605, in get_node_setting
       return objects_module.settings.get_node_setting(self.khoros_object, setting_name, node_id, node_type, v1,
     File "/Users/johndoe/Development/khoros/khoros/objects/settings.py", line 58, in get_node_setting
       setting_value = _get_v1_node_setting(khoros_object, setting_name, node_id, node_type)
     File "/Users/johndoe/Development/khoros/khoros/objects/settings.py", line 125, in _get_v1_node_setting
       raise errors.exceptions.GETRequestError(status_code=_settings_data['error']['code'],
   khoros.errors.exceptions.GETRequestError: The GET request returned the 101 status code with the following message: No board with the specified dispid.

When this error message is received, you should first ask yourself if the node being queried
matches the node type defined in the parameter. For example, the query above does not have a
node type defined in the parameter, which means it is defaulting to the ``board`` type. However,
the node in question in this circumstance is a group hub, which would explain the error.

|
