##############################
Performing Community API Calls
##############################
.. warning:: This page is still in progress and sections may be missing or unfinished.

Using the Khoros Python API to perform Community API calls is easier than doing
so manually with the `requests <https://2.python-requests.org/en/master/>`_ library
for several reasons, including:

* It is unnecessary to pass the entire URL as the base URL is stored in the :py:class:`khoros.core.Khoros`
  object. This means the relative URL passed in functions is generally the same that would be passed to
  the `rest <https://developer.khoros.com/khoroscommunitydevdocs/reference/rest>`_ or
  `restadmin <https://developer.khoros.com/khoroscommunitydevdocs/reference/restadmin>`_ FreeMarker
  directives in components, macros or endpoints.
* The authorization token (e.g. `li-api-session-key`) is automatically included in the request header
  for all API calls.
* Errors and exceptions are more intuitive with Khoros-specific messages.

There are three types of API calls that can be made using the :py:class:`khoros.core.Khoros` object:

* `Community API v1 calls`_
* `Community API v2 calls`_
* Generic API calls

.. include:: embed/instantiate-object.rst

**********************
Community API v1 calls
**********************
You can perform
`Khoros Community API v1 <https://developer.khoros.com/khoroscommunitydevdocs/docs/getting-started-with-api-1>`_
calls using the methods contained within the
:py:class:`khoros.core.Khoros.V1` class:

* Use the :py:meth:`khoros.core.Khoros.V1.get` method to perform **GET** requests.
* Use the :py:meth:`khoros.core.Khoros.V1.post` method to perform **POST** requests.
* Use the :py:meth:`khoros.core.Khoros.V1.search` method to perform searches using the v1 API.

|

Performing a v1 GET request
===========================
When performing a GET request using the Community API v1, you can simply pass the relative URI
of the endpoint you wish to query.

Although API v1 responses are in XML format by default, this library converts the responses to
JSON format by default, converts the JSON string to a Python dictionary and prunes the response
to the value you need so that it is not required to do so manually.

.. code-block:: python

   >>> khoros.v1.get('/users/online/count')
   {'response': {'status': 'success', 'value': {'type': 'int', '$': 544}}}

However, if you prefer to receive your responses in XML format, you need only pass the keyword
argument ``return_json=False`` in the method call. The response will be a
`requests.models.Response <https://2.python-requests.org/en/master/user/advanced/#id2>`_ object
and including ``.text`` will provide the actual XML response.

.. code-block:: python

   >>> response = khoros.v1.get('/users/online/count', return_json=False)
   >>> type(response)
   <class 'requests.models.Response'>
   >>> response
   <Response [200]>
   >>> response.text
   '<response status="success">\n  <value type="int">551</value>\n</response>\n'

:doc:`Return to Top <community-api-calls>`

|

Performing a v1 POST request
============================
Performing Community API v1 POST requests using the library are also very simple,
requiring only a relative URI and a dictionary of query parameters and their
respective values.

.. code-block:: python

   >>> khoros.v1.post('/users/id/216/profiles/name/signature/set',
   ... {'value': 'Joe Customer, PMP '})
   {'response': {'status': 'success'}}

As with the :ref:`GET requests <community-api-calls:Performing a v1 GET request>`, the
response will be returned in JSON format by default unless the ``return_json=False``
argument is passed in the method.

.. code-block:: python

   >>> khoros.v1.post('/users/id/216/profiles/name/signature/set',
   ... {'value': 'Joe Customer, PMP'}, return_json=False).text
   '<response status="success"/>\n'

.. note::
   In order to avoid exceeding URI limits when passing large query parameters in a POST
   request, which would result in responses with ``413`` or ``414`` status codes, by
   default the query parameters are passed as a URL-encoded string in the message body
   rather than in the URI.

   However, you can still pass the query parameters in the URI
   if desired by passing the keyword argument ``params_in_uri=True`` in the method.

:doc:`Return to Top <community-api-calls>`

|

**********************
Community API v2 calls
**********************
The primary benefit introduced with the
`Khoros Community API v2 <https://developer.khoros.com/khoroscommunitydevdocs/docs/getting-started-with-community-api-2-1>`_
is the ability to leverage the
`Lithium Query Language (LiQL) <https://developer.khoros.com/khoroscommunitydevdocs/docs/using-liql>`_
to perform GET requests.

This Python library provides two options for performing LiQL queries. The first is to
provide the full LiQL query as a string argument using the :py:meth:`khoros.core.Khoros.query`
method, and the second is to pass separate arguments for the LiQL elements into the
:py:meth:`khoros.core.Khoros.search` method which constructs the LiQL query for you.

|

Using LiQL queries and the *query* method
=========================================
If you are familiar and comfortable with the
`LiQL syntax <https://developer.khoros.com/khoroscommunitydevdocs/docs/using-liql>`_
then you may prefer to construct your own LiQL queries when performing v2 GET requests.

This can be done by leveraging the :py:meth:`khoros.core.Khoros.query` method in the
core object, as demonstrated below.

.. code-block:: python

   >>> query = "SELECT login FROM users WHERE id = '216'"
   >>> khoros.query(query)
   {'status': 'success', 'message': '', 'http_code': 200,
   'data': {'type': 'users', 'list_item_type': 'user', 'size': 1,
   'items': [{'type': 'user', 'login': 'joeCustomer'}]}, 'metadata': {}}

Because the Community API v2 returns data in JSON format by default, the same can
be said for this library.


:doc:`Return to Top <community-api-calls>`

|

Passing search parameters to the *search* method
================================================
If you are not very comfortable with LiQL syntax (or just want an easy way to
perform LiQL queries) then you can use the :py:meth:`khoros.core.Khoros.search`
method to pass LiQL elements and allow the LiQL query to be constructed for you
behind-the-scenes.

The arguments that can be utilized in the method to construct the LiQL query are
listed in the table below.

=================  ===========================  ================================================================================
Argument           Data Type(s)                 Description
=================  ===========================  ================================================================================
``select_fields``  str, tuple, list, set        One or more fields to be selected within the SELECT statement (e.g. ``id``)
``from_source``    str                          The source of the data to use in the FROM statement (e.g. ``messages``)
``where_filter``   str, tuple, list, dict, set  The filters (if any) to use in the WHERE clause (e.g. ``id = '2'``)
``order_by``       str, tuple, set, dict, list  The field(s) by which to order the response data (optional)
``order_desc``     bool                         Defines if the ORDER BY directionality is DESC (default) or ASC
``limit``          int                          Allows an optional limit to be placed on the response items (ignored by default)
=================  ===========================  ================================================================================

In addition to the arguments above, you can also utilize the optional arguments below
to further customize the request and/or response.

=====================  ============  ================================================================================
Argument               Data Type(s)  Description
=====================  ============  ================================================================================
``return_json``        bool          Setting to ``False`` will return the
                                     `requests.models.Response <https://2.python-requests.org/en/master/user/advanced/#id2>`_ object
``pretty_print``       bool          Defines if the response should be "pretty printed" (``False`` by default)
``track_in_lsi``       bool          Defines if the query should be tracked within LSI, aka Khoros Community
                                     Analytics (``False`` by default)
``always_ok``          bool          Ensures that the API response always returns a ``200 OK`` status code even when
                                     the request fails (``False`` by default)
``error_code``         str           Allows an error code to optionally be supplied for testing purposes (ignored by default)
``format_statements``  bool          Determines if statements (e.g. ``SELECT``, ``FROM``, et.) should be formatted to be in
                                     all caps (``True`` by default)
=====================  ============  ================================================================================

.. note::
   These arguments above are also available in the :py:meth:`khoros.core.Khoros.query` method.

To demonstrate how this method works, let us consider the LiQL query
``SELECT login FROM users WHERE id = '216'`` that was used in the
:ref:`example <community-api-calls:Passing search parameters to the *search* method>`
for the :py:meth:`khoros.core.Khoros.query` method. The code snippet
below shows how the same query could be performed using the
:py:meth:`khoros.core.Khoros.search` method.

.. code-block:: python

   >>> khoros.search('login', 'users', 'id = "216"')
   {'status': 'success', 'message': '', 'http_code': 200,
   'data': {'type': 'users', 'list_item_type': 'user', 'size': 1,
   'items': [{'type': 'user', 'login': 'joeCustomer'}]}, 'metadata': {}}

:doc:`Return to Top <community-api-calls>`

|

*****************
Generic API calls
*****************

.. todo:: Coming soon!

:doc:`Return to Top <community-api-calls>`