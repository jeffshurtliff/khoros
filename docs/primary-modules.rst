###############
Primary Modules
###############
This section provides details around the primary modules used in the **khoros** package,
which are listed below.

* `Init Module (khoros)`_
* `Core Module (khoros.core)`_
    * `Core Structure Subclasses (khoros.core.Khoros)`_
        * `Category Subclass (khoros.core.Khoros.Category)`_
        * `Community Subclass (khoros.core.Khoros.Community)`_
        * `Node Subclass (khoros.core.Khoros.Node)`_
    * `Core Object Subclasses (khoros.core.Khoros)`_
        * `Album Subclass (khoros.core.Khoros.Album)`_
        * `Message Subclass (khoros.core.Khoros.Message)`_
        * `Role Subclass (khoros.core.Khoros.Role)`_
        * `User Subclass (khoros.core.Khoros.User)`_
* `API Module (khoros.api)`_
* `Auth Module (khoros.auth)`_
* `LiQL Module (khoros.liql)`_
* `Structures Module (khoros.structures)`_
    * `Base Structures Module (khoros.structures.base)`_
    * `Categories Module (khoros.structures.categories)`_
    * `Communities Module (khoros.structures.communities)`_
    * `Nodes Module (khoros.structures.nodes)`_
* `Objects Module (khoros.objects)`_
    * `Base Objects Module (khoros.objects.base)`_
    * `Albums Module (khoros.objects.albums)`_
    * `Attachments Module (khoros.objects.attachments)`_
    * `Messages Module (khoros.objects.messages)`_
    * `Roles Module (khoros.objects.roles)`_
    * `Users Module (khoros.objects.users)`_

|

********************
Init Module (khoros)
********************
This module (being the primary ``__init__.py`` file for the library) provides a
"jumping-off-point" to initialize the primary :py:class:`khoros.core.Khoros` object.

.. automodule:: khoros
   :members: Khoros
   :special-members: __init__

:doc:`Return to Top <primary-modules>`

|

*************************
Core Module (khoros.core)
*************************
This module contains the core object and functions to establish the connection to the API
and leverage it to perform various actions.

.. automodule:: khoros.core
   :members:
   :special-members: __init__

:doc:`Return to Top <primary-modules>`

|

Core Structure Subclasses (khoros.core.Khoros)
==============================================
The classes below are inner/nested classes within the core :py:class:`khoros.core.Khoros` class.

.. note:: The classes themselves are *CamelCase* format and singular (e.g. ``Node``, ``Category``, etc.) whereas the
          names used to call the inner class methods are all *lowercase* (or *snake_case*) and plural. (e.g.
          ``core_object.nodes.get_node_id()``, ``core_object.categories.get_category_id()``, etc.)

Category Subclass (khoros.core.Khoros.Category)
-----------------------------------------------
.. autoclass:: khoros.core::Khoros.Category
   :members:

:doc:`Return to Top <primary-modules>`

|

Community Subclass (khoros.core.Khoros.Community)
-------------------------------------------------
.. autoclass:: khoros.core::Khoros.Community
   :members:

:doc:`Return to Top <primary-modules>`

|

Node Subclass (khoros.core.Khoros.Node)
---------------------------------------
.. autoclass:: khoros.core::Khoros.Node
   :members:

:doc:`Return to Top <primary-modules>`

|

Core Object Subclasses (khoros.core.Khoros)
===========================================
The classes below are inner/nested classes within the core :py:class:`khoros.core.Khoros` class.

.. note:: The classes themselves are *CamelCase* format and singular (e.g. ``Role``, ``User``, etc.) whereas the names
          used to call the inner class methods are all *lowercase* (or *snake_case*) and plural. (e.g.
          ``core_object.roles.get_role_id()``, ``core_object.users.create()``, etc.)

Album Subclass (khoros.core.Khoros.Album)
-----------------------------------------
.. autoclass:: khoros.core::Khoros.Album
   :members:

:doc:`Return to Top <primary-modules>`

|

Message Subclass (khoros.core.Khoros.Message)
---------------------------------------------
.. autoclass:: khoros.core::Khoros.Message
   :members:

:doc:`Return to Top <primary-modules>`

|

Role Subclass (khoros.core.Khoros.Role)
---------------------------------------
.. autoclass:: khoros.core::Khoros.Role
   :members:

:doc:`Return to Top <primary-modules>`

|

User Subclass (khoros.core.Khoros.User)
---------------------------------------
.. autoclass:: khoros.core::Khoros.User
   :members:

:doc:`Return to Top <primary-modules>`

|

***********************
API Module (khoros.api)
***********************
This module handles interactions with the Khoros Community REST APIs.

.. automodule:: khoros.api
   :members:

:doc:`Return to Top <primary-modules>`

|

*************************
Auth Module (khoros.auth)
*************************
This module contains functions that facilitate authenticating to Khoros Community environments.

.. automodule:: khoros.auth
   :members:

:doc:`Return to Top <primary-modules>`

|

*************************
LiQL Module (khoros.liql)
*************************
This module contains functions that enable API queries using the LiQL syntax.

.. automodule:: khoros.liql
   :members:

:doc:`Return to Top <primary-modules>`

|

*************************************
Structures Module (khoros.structures)
*************************************
This module contains sub-modules that are specific to the various Community structures.

.. automodule:: khoros.structures
   :members:

:doc:`Return to Top <primary-modules>`

|

Base Structures Module (khoros.structures.base)
===============================================
This module contains functions relating to structures. (i.e. categories, nodes and tenants/communities)

.. automodule:: khoros.structures.base
   :members:

:doc:`Return to Top <primary-modules>`

|

Categories Module (khoros.structures.categories)
================================================
This module contains functions specific to categories within the Khoros Community platform.

.. automodule:: khoros.structures.categories
   :members:

:doc:`Return to Top <primary-modules>`

|

Communities Module (khoros.structures.communities)
==================================================
This module contains functions specific to the high-level community configuration.

.. automodule:: khoros.structures.communities
   :members:

:doc:`Return to Top <primary-modules>`

|

Nodes Module (khoros.structures.nodes)
======================================
This module contains functions specific to nodes within the Khoros Community platform.

.. automodule:: khoros.structures.nodes
   :members:

:doc:`Return to Top <primary-modules>`

|

*******************************
Objects Module (khoros.objects)
*******************************
This module contains sub-modules that are specific to the various Community API objects.

.. automodule:: khoros.objects
   :members:

:doc:`Return to Top <primary-modules>`

|

Base Objects Module (khoros.objects.base)
=========================================
This module contains functions that relate to the various Community API objects but which are object-agnostic.

.. automodule:: khoros.objects.base
   :members:

:doc:`Return to Top <primary-modules>`

|

Albums Module (khoros.objects.albums)
=====================================
This module includes functions that handle albums that contain images.

.. automodule:: khoros.objects.albums
   :members:

:doc:`Return to Top <primary-modules>`

|

Attachments Module (khoros.objects.attachments)
===============================================
This module includes functions that handle attachments for messages.

.. automodule:: khoros.objects.attachments
   :members:

:doc:`Return to Top <primary-modules>`

|

Messages Module (khoros.objects.messages)
=========================================
This module includes functions that handle messages within a Khoros Community environment.

.. automodule:: khoros.objects.messages
   :members:

:doc:`Return to Top <primary-modules>`

|

Roles Module (khoros.objects.roles)
===================================
This module includes functions that handle roles and permissions.

.. automodule:: khoros.objects.roles
   :members:

:doc:`Return to Top <primary-modules>`

|

Users Module (khoros.objects.users)
===================================
This module includes functions that handle user-related operations.

.. automodule:: khoros.objects.users
   :members:

:doc:`Return to Top <primary-modules>`

|