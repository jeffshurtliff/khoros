#######################
Working with Group Hubs
#######################
Group Hubs are nodes with unique capabilities that can be leveraged in ways unlike
any other board within the Khoros Community platform. This section addresses how
the Khoros Community Python library leverages the API to harness these nodes.

* `Overview`_
* `Creating a New Group Hub`_
    * `Return Options`_
        * `Simple Boolean Response (Default)`_
        * `Full API Response`_
        * `Return the ID`_
        * `Return the URL`_
        * `Return the API URL`_
        * `Return the API Response HTTP Code`_
        * `Return the API Response Status`_
        * `Return Any Error Messages`_
        * `Return Multiple Types`_
    * `Defining the ID and Title`_

|

********
Overview
********
Group Hubs are one of the newer features (as of May 2020) in the Khoros Community platform,
with their general availability and Khoros Community API v2 support for them having been introduced as part of the
`Khoros Communities 20.1 Release <https://community.khoros.com/t5/Khoros-Community-Release-Notes/Khoros-Communities-20-1-Release-Notes/ba-p/565249>`_
in January 2020.

This node, which behaves in similar ways to a `Facebook group <https://www.facebook.com/help/1629740080681586>`_,
has a few
`key differences <https://community.khoros.com/t5/Khoros-Community-Blog/Group-Hubs-Overview-and-Use-Cases/ba-p/561969>`_
compared to other boards, including the following:

* Group hubs can include any discussion type
* Group hubs can be **Open**, **Closed** or **Hidden**
* Users can be granted the ability to create their own groups if desired

|

************************
Creating a New Group Hub
************************
Creating a new Group Hub is similar to :ref:`creating a new board <boards:Creating a New Board>`
except with fewer configuration options during the actual creation.  For example, you are not
able to specify in the API request to create a group hub who its members should be, how labels
should be leveraged, who its moderators will be, etc. However, you will be able to define the
following:

* :ref:`Node ID <group-hubs:Defining the ID and Title>` *
* :ref:`Title <group-hubs:Defining the ID and Title>` *
* Description
* Membership Type*
* Discussion Styles
* Parent Category ID
* Avatar Image

.. note:: The fields labeled with an asterisk (*) are required.

:doc:`Return to Top <group-hubs>`

Return Options
==============
There are multiple ways to return data when creating a group hub, which can be
explicitly defined using one or more of the following function arguments:

* :ref:`full_response <group-hubs:Full API Response>`
* :ref:`return_id <group-hubs:Return the ID>`
* :ref:`return_url <group-hubs:Return the URL>`
* :ref:`return_api_url <group-hubs:Return the API URL>`
* :ref:`return_http_code <group-hubs:Return the API Response HTTP Code>`
* :ref:`return_status <group-hubs:Return the API Response Status>`
* :ref:`return_error_messages <group-hubs:Return Any Error Messages>`

These arguments are explained in more detail within the sub-sections below.

:doc:`Return to Top <group-hubs>`

|

Simple Boolean Response (Default)
---------------------------------
Unless explicitly defined, the function will return a simple Boolean response
(i.e. ``True`` or ``False``) indicating whether or not the operation was successful.

.. code-block:: python

   >>> def create_and_check():
   ...     successful = khoros.grouphubs.create('my-new-group', 'My New Group', open_group=True)
   ...     result = "It worked!" if successful else "It failed!"
   ...     print(result)
   ...

   >>> create_and_check()
   'It worked!'

:doc:`Return to Top <group-hubs>`

|

Full API Response
-----------------
If you'd rather return the full, raw response from the API request in order to parse
it later at your convenience, then this can be done by setting the ``full_response``
argument to ``True`` in the function call as shown below.

.. code-block:: python

   >>> response = khoros.grouphubs.create('my-new-group', 'My New Group', open_group=True, full_response=True)
   >>> if response.status_code != 404:
   ...     response = response.json()
   ...     print(response['status'])
   'success'

:doc:`Return to Top <group-hubs>`

|

Return the ID
-------------
If it makes sense for you to return the ID of the group hub you just created then
you can do so by defining the ``return_id`` argument as ``True`` as seen below.

.. code-block:: python

   >>> groups_to_create = [('first-group', 'My First Group'), ('second-group', 'My Second Group')]
   >>> for group in groups_to_create:
   ...     group_id, group_title = group
   ...     group_id = khoros.grouphubs.create(group_id, group_title, open_group=True, return_id=True)
   ...     print("Group Hub Created:", group_id)
   'Group Hub Created: first-group'
   'Group Hub Created: second-group'

:doc:`Return to Top <group-hubs>`

|

Return the URL
--------------
Very likely the most popular return option for this function, defining the ``return_url``
argument as ``True`` will return the URL of the newly created group hub, as shown below.

.. code-block:: python

   >>> khoros.grouphubs.create('python-lovers', 'The Python Lovers Group', \
   ... open_group=True, return_url=True)
   'https://stage.example.com/t5/the-python-lovers-group/gh-p/python-lovers'

:doc:`Return to Top <group-hubs>`

|

Return the API URL
------------------
If additional API calls will be immediately performed following the creation of a board,
it may be useful to return the API URL (i.e. URI) for the new board by defining the
``return_api_url`` argument as ``True``, as shown below.

.. code-block:: python

   >>> khoros.grouphubs.create('python-lovers', 'The Python Lovers Group', \
   ... open_group=True, return_api_url=True)
   '/grouphubs/python-lovers'

:doc:`Return to Top <group-hubs>`

|

Return the API Response HTTP Code
---------------------------------
Another potentially useful return option is to define the ``return_http_code``
argument as ``True``, which will return the
`HTTP status code <https://en.wikipedia.org/wiki/List_of_HTTP_status_codes>`_
for the API response, as demonstrated below.

.. code-block:: python

   >>> khoros.grouphubs.create('python-lovers', 'The Python Lovers Group', \
   ... open_group=True, return_http_code=True)
   200

:doc:`Return to Top <group-hubs>`

|

Return the API Response Status
------------------------------
Alternatively, it is possible to return the status of the API response (as defined
by Khoros in the JSON response) by defining the ``return_status`` argument as
``True``, as shown below.

.. code-block:: python

   >>> khoros.grouphubs.create('my-first-group', 'My First Group', \
   ... open_group=True, return_status=True)
   'success'

   >>> khoros.grouphubs.create('my-first-group', 'My First Group', \
   ... open_group=True, return_status=True)
   'error'

:doc:`Return to Top <group-hubs>`

|

Return Any Error Messages
-------------------------
If you want to ensure that you see any error messages when applicable but don't want to
return the full API response, you can define the ``return_error_messages`` argument as
``True``, as shown below.

.. code-block:: python

   >>> khoros.grouphubs.create('my-first-group', 'My First group', \
   ... open_group=True, return_error_messages=True)
   "An object of type grouphub already exists with the 'id' property value 'my-first-group'"

This argument captures both the ``message`` value and the occasionally populated
``developer_message`` value. If one of the values is blank or if they are exactly the same, such
as in the example above, then only one of the values will be displayed. Otherwise, if both values
are defined and do not match then they will be returned in the ``{message} - {developer_message}``
format.  (i.e. The two values will be separated by spaces and a hyphen.)

If you wish to return both fields regardless of their values then you can define the optional
``split_errors`` argument as ``True`` as well to return a tuple containing both values, as shown
below.

.. code-block:: python

   >>> khoros.grouphubs.create('my-first-blog', 'My First Blog', open_group=True, \
   ... return_error_messages=True, split_errors=True)
   ("An object of type grouphub already exists with the 'id' property value 'my-first-group'", "An object of type grouphub already exists with the 'id' property value 'my-first-group'")

:doc:`Return to Top <group-hubs>`

|

Return Multiple Types
---------------------
You are not restricted to choosing only one of the return options. You can enable as many options as needed and if
multiple types are detected by the function then they will be returned as a tuple with those values, as demonstrated
in the example below.

.. code-block:: python

   >>> response = khoros.grouphubs.create('my-first-group', 'My First group', open_group=True, \
   ... return_http_code=True, return_status=True, return_error_messages=True)

   >>> if response[1] == 'success':
   ...     print(f"The group hub creation was successful with the HTTP code {response[0]}.")
   ... else:
   ...     print(f"The group hub creation failed with the following error:\n{response[2]}")
   ...
   The group hub creation failed with the following error:
   An object of type grouphub already exists with the 'id' property value 'my-first-group'

.. note:: The tuple will return the values in the order they are listed as function arguments.

:doc:`Return to Top <group-hubs>`

|

Defining the ID and Title
=========================
The ID and Title for the new group hub are defined using the ``group_hub_id`` and ``group_hub_title``
arguments, respectively, as demonstrated in the example below.

.. code-block:: python

   >>> khoros.grouphubs.create('this-is-the-id', 'This is the Group Title', open_group=True)

.. note:: Because ``group_hub_id`` is the first argument and ``group_hub_title`` is the
          second argument in the function/method, it is not necessary to use keyword arguments
          (e.g. ``group_hub_id='this-is-the-id'``) to designate each argument.

:doc:`Return to Top <group-hubs>`

|

.. todo:: This page is currently being developed. Please check back later for more information.
