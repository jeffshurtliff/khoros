##############################
Performing Community API Calls
##############################
.. warning:: This page is still in progress and sections may be missing or unfinished.

Using the Khoros Python API to perform Community API calls is easier than doing
so manually with the *requests* library for several reasons, including:

* It is unnecessary to pass the entire URL as the base URL is stored in the :py:class:`khoros.core.Khoros` object. This means the relative URL passed in functions is generallu the same that would be passed to the *rest* or *restadmin* FreeMarker directives in components, macros or endpoints.
* The authorization token (e.g. `li-api-session-key`) is automatically included in the request header for all API calls.
* Errors and exceptions are more intuitive with Khoros-specific messages.

There are three types of API calls that can be made using the :py:class:`khoros.core.Khoros` object:

* `Community API v1 calls`_
* Community API v2 calls
* Generic API calls

|

**********************
Community API v1 calls
**********************
You can perform Khoros Community API v1 calls using the methods contained within the :py:class:`khoros.core.Khoros.V1` class:

* Use the :py:meth:`khoros.core.Khoros.V1.get` method to perform **GET** requests.
* Use the :py:meth:`khoros.core.Khoros.V1.post` method to perfork **POST** requests.
* Use the :py:meth:`khoros.core.Khoros.V1.search` method to perform searches using the v1 API.

.. todo:: Add introductory section on instantiating the main object as *khoros*.

|

Performing a v1 GET request
===========================
When performing a GET request using the Community API v1, you can simply pass the relative URI of the endpoint you wish to query.

.. todo:: Add specific example and code snippet

Although API v1 responses are in XML format by default, this library converts the responses to JSON format by default, converts
the JSON string to a Python dictionary and prunes the response to the value you need so
that it is not required to do so manually.

.. todo:: Add specific example and code snippet

However, if you prefer to receive your responses in XML format, you need only pass
the keyword argument ``return_json=False`` in the method call.

.. todo:: Add specific example and code snippet





