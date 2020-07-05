#####################
Working with Messages
#####################
.. caution:: This page is currently a work-in-progress and is subject to change without warning.

This page provides instructions on how to create, update and perform other operations
relating to messages. 

* `Introduction`_
* `Prerequisites`_
* `Creating new messages`_

|

************
Introduction
************

A message is arguably the most important object within a Khoros Community, as a
message is the base object representing all user-created assets (i.e. content) in the
environment. 

Messages represent multiple *discussion styles* (i.e. content types) depending on
the :doc:`board <boards>` in which it is published, including:

* blog posts (aka *blog articles*)
* forum/discussion threads
* knowledge articles (aka *TKB articles*)
* contests
* ideas
* Q&A articles

This page explains how to work with message via the :py:mod:`khoros` Python library.

|

*************
Prerequisites
*************
As with most other methods and functions, the
:ref:`core Khoros object <introduction:Initializing a Khoros object instance>`
must be instantiated so that it can be leveraged to perform the authenticated and
authorized API calls. 

Performing this task is covered in detail on the :doc:`introduction` page, and is
demonstrated briefly in the examples below. 

|

Instantiation using environment variables
=========================================
If you have defined environment variables for your Khoros Community
environment on your system from which you are leveraging the library
then it is very eaay to instantiate the
:ref:`core Khoros object <introduction:Initializing a Khoros object instance>` 
as shown below. 

.. code-block:: python

   from khoros import Khoros
   khoros = Khoros()

.. note:: As mentioned on other pages, it is recommended that you use ``khoros``
          as the identifier for the instantiated object.

|

Instantiation using a helper file
=================================
If environment variables are not configured, the next simplest option is to use a
:ref:`helper file <introduction:Leveraging a "helper" configuration file>`
as demonstrated below.

.. code-block:: python

   from khoros import Khoros
   khoros = Khoros(helper='path/to/helper.yml')

|

Manual instantiation
====================
In the absence of environment variables or a helper file, the
:ref:`core Khoros object <introduction:Initializing a Khoros object instance>`
can be instantiated manually using the :py:class:`khoros.core.Khoros`
``__init__`` method arguments. This is illustrated in the sample code found on the
:ref:`Introduction <introduction:Passing the information directly into the object>` page.

|

*********************
Creating new messages
*********************
Creating new messages can be done using the
:py:meth:`khoros.core.Khoros.Message.create` method within the
:ref:`core Khoros object <introduction:Initializing a Khoros object instance>`,
which can be called using the ``khoros.messsages.create` method, assuming
``khoros`` is the name of the instantiated core object per the recommended practice.

At a minimum, creating a new message requires the following elements:

* Subject (i.e. title)
* Destination (i.e. board in which it will be published)

.. note:: It is interesting to note that, unlike other community platforms
          (including `Khoros JX <https://khorosjx.rtfd.io>`_),
          the content body is **not** a required field.

However, in the examples within this tutorial a message body will be provided
to further clarify the process.

Defining the node
=================
.. todo:: Coming Soon!




