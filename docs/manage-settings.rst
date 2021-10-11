######################
Managing Node Settings
######################
You can manage the settings on any node (including categories, boards and grouphubs)
using the :py:class:`khoros.core.Khoros.Settings` subclass, which leverages the
:py:mod:`khoros.objects.settings` module.

This guide demonstrates various ways that you can retrieve, define and update the
node settings within your Khoros Communities environment.

|

*************
Prerequisites
*************
Throughout this guide we will assume that the Khoros core object has already been
instantiated as ``khoros`` as shown below.

.. code-block:: python

   >>> from khoros import Khoros
   >>> khoros = Khoros(helper='/Users/example/helper.yml')

|

Retrieving node settings
========================
This section demonstrates how easy it is to retrieve a specific setting value from a node.

.. caution::
   These methods and functions assume you are querying a **board** by default.
   An additional parameter must be passed in order to query a **category** or
   **grouphub** node, as will be explained.

|

Retrieving board settings
-------------------------
A specific setting for a board can be retrieved using the
:py:class:`khoros.core.Khoros.Settings.get_node_setting` method, which leverages the
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

   >>> khoros.settings.get_node_setting('c_primary_moderator', 'product-blog')
   'cmmgr123'
   >>> khoros.settings.get_node_setting('custom.primary_moderator', 'product-blog')
   'cmmgr123'

However, if you want to ensure that the appropriate API version is leveraged then you can explicitly
define it using the ``v1`` parameter by defining it as either ``True`` or ``False``.

.. code-block:: python

   >>> khoros.settings.get_node_setting('c_primary_moderator', 'product-blog', v1=False)
   'cmmgr123'
   >>> khoros.settings.get_node_setting('custom.primary_moderator', 'product-blog', v1=True)
   'cmmgr123'

|

Retrieving category settings
----------------------------
Retrieving a node setting from a category is nearly identical to retrieving board settings, with the
one caveat that you must explicitly define the node type in the third parameter, as illustrated below.

.. code-block:: python

   >>> khoros.settings.get_node_setting('c_primary_moderator', 'our-awesome-product', 'category')
   'cmmgr123'
   >>> khoros.settings.get_node_setting('custom.primary_moderator', 'our-awesome-product', 'category')
   'cmmgr123'

.. caution::

   It is important to note that the node type should be defined in **singular form** rather than in
   **plural**.  This means that ``category``, ``board`` and ``grouphub`` are the three acceptable values.

|

Retrieving group hub settings
-----------------------------
Similar to retrieving category settings, you must explicitly define the node type using the ``grouphub`` value
to successfully retrieve the value, as demonstrated below.

.. code-block:: python

   >>> khoros.settings.get_node_setting('c_primary_moderator', 'api-users-group', 'grouphub')
   'cmmgr123'
   >>> khoros.settings.get_node_setting('custom.primary_moderator', 'api-users-group', 'grouphub')
   'cmmgr123'

