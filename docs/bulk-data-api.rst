##############################
Performing Bulk Data API Calls
##############################
.. warning:: This page is still in progress and sections may be missing or unfinished.

The Khoros Communities
`Bulk Data API <https://community.khoros.com/t5/Community-Analytics/Using-the-Khoros-Bulk-Data-API/ta-p/178715>`_
is a very useful tool for retrieving analytical data for your community, and this SDK can
be leveraged to query the Bulk Data API using Python.

.. seealso:: For additional information on how to leverage the Bulk Data API, refer to the
             `Khoros Developer Documentation <https://developer.khoros.com/khoroscommunitydevdocs/reference/bulk-data-api-v2>`_.

.. include:: embed/instantiate-object.rst

This guide covers the following topics:

* `Connecting to the API`_
    * `During Instantiation`_
    * `Using a Helper File`_
* `Querying the Bulk Data API`_

|

*********************
Connecting to the API
*********************
In order to connect to the
`Bulk Data API <https://community.khoros.com/t5/Community-Analytics/Bulk-Data-API-FAQs/ta-p/438764>`_,
you will need to sign into the
`Community Analytics <https://community.khoros.com/t5/Community-Analytics/Getting-around-Community-Analytics/ta-p/109889>`_
(formerly called *Lithium Social Intelligence* or *LSI*) user interface, click on your username in the
top-right corner and retrieve your connection information. This information includes the following:

* Community ID
* Client ID
* Access Token

There are then two ways that you can supply this information in the Python SDK, which are covered in the
sections below.

* `During Instantiation`_
* `Using a Helper File`_

|

During Instantiation
====================
When instantiating the core object, you can supply the Bulk Data API connection information using the
``bulk_data_settings`` parameter, as shown below.

.. code-block:: python

   >>> bulk_data_settings = {
       'community_id': 'example.prod',
       'client_id': 'ay0CXXXXXXXXXX/XXXX+XXXXXXXXXXXXX/XXXXX4KhQ=',
       'token': '2f25XXXXXXXXXXXXXXXXXXXXXXXXXa10dec04068',
   }
   >>> khoros = Khoros(defined_settings=settings, bulk_data_settings=bulk_data_settings, auto_connect=False)

|

Using a Helper File
===================
Similar to how a helper file can be used to connect to the standard Community APIs, a helper file can be
used to supply the connection information for the Bulk Data API. If the helper file is supplied in YAML
format then it will appear similar to the example below.

.. code-block:: yaml

   # Define how to obtain the connection information
   connection:
       # Bulk Data API connection information
       bulk_data:
           community_id: example.prod
           client_id: ay0CXXXXXXXXXX/XXXX+XXXXXXXXXXXXX/XXXXX4KhQ=
           token: 2f25XXXXXXXXXXXXXXXXXXXXXXXXXa10dec04068
           europe: no

|

**************************
Querying the Bulk Data API
**************************

.. todo:: This section will be written soon

