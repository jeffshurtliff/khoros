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
then it is very easy to instantiate the
:ref:`core Khoros object <introduction:Initializing a Khoros object instance>` 
as shown below. 0

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
which can be called using the ``khoros.messages.create`` method, assuming
``khoros`` is the name of the instantiated core object per the recommended practice.

At a minimum, creating a new message requires the following elements:

* Subject (i.e. title)
* Destination (i.e. board in which it will be published)

.. note:: It is interesting to note that, unlike other community platforms
          (including `Khoros JX <https://khorosjx.rtfd.io>`_),
          the content body is **not** a required field.

However, in the examples within this tutorial, a message body will be provided
to further clarify the process.

Defining the node
=================
The node can be defined by providing one of these artifacts:
* A node collection object
* A node ID
* A node URL

A node collection object is a dictionary with fields defining the node, which can be
obtained from other queries or can be constructed manually. For it to be valid, it
must have an ``id`` field with the Node ID as the corresponding value.

Node collection objects can be passed to the ``khoros.messages.create`` method using
the ``node`` parameter.

Unless you already have retrieved the node collection (or have the node ID in a
similarly structured dictionary) then it is generally easier to simply provide the
Node ID via the ``node_id`` parameter or the node URL via the ``node_url`` parameter.

Identifying other parameters
============================
There are several other optional parameters you can pass in the method when creating
messages, which are listed below.

==================== ====== ===========================================
Parameter            Type   Description
==================== ====== ===========================================
``body``             string The body of the message as text or HTML
``canonical_url``    string The Canonical URL for SEO purposes
``context_id``       string The Context ID field
``context_url``      string The Context URL field
``cover_image``      dict   Image collection object for the Cover Image
``images``           dict   Images to be added to the message
``is_answer``        bool   Designates as answer on a Q&A board
``is_draft``         bool   Identifies the message as a draft
``labels``           dict   Labels associated with the message
``product_category`` dict   Associated product category
``products``         dict   Associated product(s) in product catalog
``read_only``        bool   Identifies the message as read-only
``seo_title``        string The SEO title
``seo_description``  string The SEO description
``tags``             dict   Tags associated with the message
``teaser``           string Message teaser (used with blog articles)
``topic``            dict   The root message associated with the post
``videos``           dict   Videos uploaded to the message
==================== ====== ===========================================

Attachments
-----------
If you are including attachments with your message, you should use the
``attachment_file_paths`` parameter to pass the absolute file path(s) to the
attachment(s).


Calling the method
==================
Calling the method is relatively easy once you have identified the parameters you wish
to include, as demonstrated below.

.. code-block:: python

   subject = 'This is my first message'
   body = '<h1>Hello World</h1>'
   node_id = 'my-blog'
   khoros.messages.create(subject=subject, body=body, node_id=node_id)

