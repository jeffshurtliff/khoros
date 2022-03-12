###############
Primary Modules
###############
This section provides details around the primary modules used in the **khoros** package,
which are listed below.

* `Init Module (khoros)`_
* `Core Module (khoros.core)`_
* `API Module (khoros.api)`_
* `Auth Module (khoros.auth)`_
* `Bulk Data Module (khoros.bulk_data)`_
* `LiQL Module (khoros.liql)`_
* `Objects Module (khoros.objects)`_
    * `Base Objects Module (khoros.objects.base)`_
    * `Albums Module (khoros.objects.albums)`_
    * `Archives Module (khoros.objects.archives)`_
    * `Attachments Module (khoros.objects.attachments)`_
    * `Labels Module (khoros.objects.labels)`_
    * `Messages Module (khoros.objects.messages)`_
    * `Roles Module (khoros.objects.roles)`_
    * `Settings Module (khoros.objects.settings)`_
    * `Subscriptions Module (khoros.objects.subscriptions)`_
    * `Tags Module (khoros.objects.tags)`_
    * `Users Module (khoros.objects.users)`_
* `SAML Module (khoros.saml)`_
* `Structures Module (khoros.structures)`_
    * `Base Structures Module (khoros.structures.base)`_
    * `Boards Module (khoros.structures.boards)`_
    * `Categories Module (khoros.structures.categories)`_
    * `Communities Module (khoros.structures.communities)`_
    * `Group Hubs Module (khoros.structures.grouphubs)`_
    * `Nodes Module (khoros.structures.nodes)`_
* `Studio Module (khoros.studio)`_
    * `Base Studio Module (khoros.studio.base)`_

|

********************
Init Module (khoros)
********************
The Init Module is covered on :doc:`this page <core-object-methods>`.

|

*************************
Core Module (khoros.core)
*************************
The Core Module is covered on :doc:`this page <core-object-methods>`.

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

***********************************
Bulk Data Module (khoros.bulk_data)
***********************************
This module contains functions that relate to the Bulk Data API.

.. automodule:: khoros.bulk_data
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

Archives Module (khoros.objects.archives)
=========================================
This module includes functions that handle the archiving of messages.

.. automodule:: khoros.objects.archives
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

Labels Module (khoros.objects.labels)
=====================================
This module includes functions that handle labels within a Khoros Community environment.

.. automodule:: khoros.objects.labels
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

Settings Module (khoros.objects.settings)
=========================================
This module includes functions that handle community, node and user settings.

.. automodule:: khoros.objects.settings
   :members:

:doc:`Return to Top <primary-modules>`

|

Subscriptions Module (khoros.objects.subscriptions)
===================================================
This module includes functions that handle subscriptions.

.. automodule:: khoros.objects.subscriptions
   :members:

:doc:`Return to Top <primary-modules>`

|

Tags Module (khoros.objects.tags)
=================================
This module includes functions that handle tags within a Khoros Community environment.

.. automodule:: khoros.objects.tags
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

*************************
SAML Module (khoros.saml)
*************************
This module includes functions that relate to SAML Single Sign-On (SSO).

.. automodule:: khoros.saml
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

Boards Module (khoros.structures.boards)
========================================
This module contains functions specific to boards within the Khoros Community platform.

.. automodule:: khoros.structures.boards
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

Group Hubs Module (khoros.structures.grouphubs)
===============================================
This module contains functions specific to group hubs within the Khoros Community platform.

.. automodule:: khoros.structures.grouphubs
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

*****************************
Studio Module (khoros.studio)
*****************************
This module contains sub-modules that relate to the Lithium SDK and the Khoros Community Studio Plugin.

.. automodule:: khoros.studio
   :members:

:doc:`Return to Top <primary-modules>`

|

Base Studio Module (khoros.studio.base)
=======================================
This module contains functions that handle the base functionality of the :py:mod:`khoros.studio` module.

.. automodule:: khoros.studio.base
   :members:

:doc:`Return to Top <primary-modules>`

|

-----

The previous page addresses :doc:`core-object-methods` within the *khoros* package.
The next page addresses the :doc:`supporting-modules` within the *khoros* package.
