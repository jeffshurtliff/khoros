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
* Community API v2 calls
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
