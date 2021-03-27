##################
Khoros Core Object
##################
This section provides details around the core module and the methods used
within the core object for the **khoros** package, which are listed below.

* `Init Module (khoros)`_
* `Core Module (khoros.core)`_
    * `Core Functionality Subclasses (khoros.core.Khoros)`_
        * `V1 Subclass (khoros.core.Khoros.V1)`_
    * `Core Object Subclasses (khoros.core.Khoros)`_
        * `Album Subclass (khoros.core.Khoros.Album)`_
        * `Message Subclass (khoros.core.Khoros.Message)`_
        * `Role Subclass (khoros.core.Khoros.Role)`_
        * `Settings Subclass (khoros.core.Khoros.Settings)`_
        * `User Subclass (khoros.core.Khoros.User)`_
    * `Core Structure Subclasses (khoros.core.Khoros)`_
        * `Board Subclass (khoros.core.Khoros.Board)`_
        * `Category Subclass (khoros.core.Khoros.Category)`_
        * `Community Subclass (khoros.core.Khoros.Community)`_
        * `Group Hub Subclass (khoros.core.Khoros.GroupHub)`_
        * `Node Subclass (khoros.core.Khoros.Node)`_
    * `Studio Subclass (khoros.core.Khoros.Studio)`_

|

********************
Init Module (khoros)
********************
This module (being the primary ``__init__.py`` file for the library) provides a
"jumping-off-point" to initialize the primary :py:class:`khoros.core.Khoros` object.

.. automodule:: khoros
   :members: Khoros
   :special-members: __init__

:doc:`Return to Top <core-object-methods>`

|

*************************
Core Module (khoros.core)
*************************
This module contains the core object and functions to establish the connection to the API
and leverage it to perform various actions.

.. automodule:: khoros.core
   :members:
   :special-members: __init__

:doc:`Return to Top <core-object-methods>`

|

Core Functionality Subclasses (khoros.core.Khoros)
==================================================
These classes below are inner/nested classes within the core :py:class:`khoros.core.Khoros` class.

.. note:: The classes themselves are *PascalCase* format and singular (e.g. ``Node``, ``Category``, etc.) whereas the
          names used to call the inner class methods are all *lowercase* (or *snake_case*) and plural.
          (e.g. ``core_object.nodes.get_node_id()``, ``core_object.categories.get_category_id()``, etc.)

Studio Subclass (khoros.core.Khoros.Studio)
-------------------------------------------
.. autoclass:: khoros.core::Khoros.Studio
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|

V1 Subclass (khoros.core.Khoros.V1)
-----------------------------------
.. autoclass:: khoros.core::Khoros.V1
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|


Core Structure Subclasses (khoros.core.Khoros)
==============================================
The classes below are inner/nested classes within the core :py:class:`khoros.core.Khoros` class.

.. note:: The classes themselves are *PascalCase* format and singular (e.g. ``Node``, ``Category``, etc.) whereas the
          names used to call the inner class methods are all *lowercase* (or *snake_case*) and plural.
          (e.g. ``core_object.nodes.get_node_id()``, ``core_object.categories.get_category_id()``, etc.)

Board Subclass (khoros.core.Khoros.Board)
-----------------------------------------
.. autoclass:: khoros.core::Khoros.Board
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|

Category Subclass (khoros.core.Khoros.Category)
-----------------------------------------------
.. autoclass:: khoros.core::Khoros.Category
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|

Community Subclass (khoros.core.Khoros.Community)
-------------------------------------------------
.. autoclass:: khoros.core::Khoros.Community
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|

Group Hub Subclass (khoros.core.Khoros.GroupHub)
------------------------------------------------
.. autoclass:: khoros.core::Khoros.GroupHub
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|

Node Subclass (khoros.core.Khoros.Node)
---------------------------------------
.. autoclass:: khoros.core::Khoros.Node
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|

Core Object Subclasses (khoros.core.Khoros)
===========================================
The classes below are inner/nested classes within the core :py:class:`khoros.core.Khoros` class.

.. note:: The classes themselves are *CamelCase* format and singular (e.g. ``Role``, ``User``, etc.) whereas the
          names used to call the inner class methods are all *lowercase* (or *snake_case*) and plural. (e.g.
          ``core_object.roles.get_role_id()``, ``core_object.users.create()``, etc.)

Album Subclass (khoros.core.Khoros.Album)
-----------------------------------------
.. autoclass:: khoros.core::Khoros.Album
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|

Message Subclass (khoros.core.Khoros.Message)
---------------------------------------------
.. autoclass:: khoros.core::Khoros.Message
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|

Role Subclass (khoros.core.Khoros.Role)
---------------------------------------
.. autoclass:: khoros.core::Khoros.Role
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|

Settings Subclass (khoros.core.Khoros.Settings)
-----------------------------------------------
.. autoclass:: khoros.core::Khoros.Settings
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|

Subscription Subclass (khoros.core.Khoros.Subscription)
-------------------------------------------------------
.. autoclass:: khoros.core::Khoros.Subscription
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|

User Subclass (khoros.core.Khoros.User)
---------------------------------------
.. autoclass:: khoros.core::Khoros.User
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|

-----

The next page addresses the :doc:`primary-modules` within the *khoros* package.
