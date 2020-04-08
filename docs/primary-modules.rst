###############
Primary Modules
###############
This section provides details around the primary modules used in the **khoros** package,
which are listed below.

* `Init Module (khoros)`_
* `Core Module (khoros.core)`_
    * `Core Object Subclasses (khoros.core.Khoros)`_
* `API Module (khoros.api)`_
* `Auth Module (khoros.auth)`_
* `LiQL Module (khoros.liql)`_
* `Objects Module (khoros.objects)`_
    * `Base Module (khoros.objects.base)`_
    * `Users Module (khoros.objects.users)`_

|

********************
Init Module (khoros)
********************
This module (being the primary ``__init__.py`` file for the library) provides a
"jumping-off-point" to initialize the primary :py:class:`khoros.core.Khoros` object.

.. automodule:: khoros
   :members: Khoros

:doc:`Return to Top <primary-modules>`

|

*************************
Core Module (khoros.core)
*************************
This module contains the core object and functions to establish the connection to the API
and leverage it to perform various actions.

.. automodule:: khoros.core
   :members:

.. autoclass:: khoros.core::Khoros.Node
   :members:

.. autoclass:: khoros.core::Khoros.User
   :members:

:doc:`Return to Top <primary-modules>`

|

Core Object Subclasses (khoros.core.Khoros)
===========================================
The classes below are inner/nested classes within the core :py:class:`khoros.core.Khoros` class.

.. note:: The classes themselves are *CamelCase* format and singular (e.g. ``Node``, ``User``, etc.) whereas the names
          used to call the inner class methods are all *lowercase* (or *snake_case*) and plural. (e.g.
          ``core_object.nodes.get_node_id()``, ``core_object.users.create()``, etc.)

.. autoclass:: khoros.core::Khoros.Node
   :members:

.. autoclass:: khoros.core::Khoros.User
   :members:

:doc:`Return to Top <primary-modules>`

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

*******************************
Objects Module (khoros.objects)
*******************************
This module contains sub-modules that are specific to the various Community API objects.

.. automodule:: khoros.objects
   :members:

:doc:`Return to Top <primary-modules>`

|

Base Module (khoros.objects.base)
=================================
This module contains functions that relate to the various Community API objects but which are object-agnostic.

.. automodule:: khoros.objects.base
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