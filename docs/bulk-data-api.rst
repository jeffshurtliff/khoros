##############################
Performing Bulk Data API Calls
##############################
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
* `Manipulating Retrieved Data`_
    * `Filtering by User Type`_
    * `Filtering by Action`_
    * `Counting Actions`_
    * `Counting Logins and Views`_


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

When performing queries against the Bulk Data API, you must provide a "From Date" and a
"To Date" and can query up to 7 days worth of data at one time. You also have the ability to
export the data in JSON or CSV format.

As such, assuming you are using a helper file to authenticate (as explained in the previous
section), you will be leveraging the ``from_date``, ``to_date``, and ``export_type`` parameters
with the :py:meth:`khoros.core.Khoros.BulkData.query` method.

For example, if you wished to capture data between October 25, 2022, and November 1, 2022, and
wished to export the data in JSON format, then you would use syntax similar to what is shown
below. The example below also demonstrates how you would export the results to a JSON file.

.. code-block:: python

   import json
   from khoros import Khoros

   # Instantiate the khoros object
   khoros = Khoros(helper='helper.yml')

   # Perform the Bulk Data API query
   results = khoros.bulk_data.query(from_date='20221025', to_date='20221101', export_type='json')

   # Export to a JSON file
   with open('path/to/bulk_data_export.json', 'w') as file:
       json.dump(results, file, indent=2)

|

***************************
Manipulating Retrieved Data
***************************
After querying the Bulk Data API, there are several ways you can easily manipulate the data
you retrieved if you exported the results in JSON format. These options are explained below.

* `Filtering by User Type`_
* `Filtering by Action`_
* `Counting Actions`_
* `Counting Logins and Views`_

|

Filtering by User Type
======================
When viewing your data, you may wish to pare the data down to only logged-in users, or perhaps
only anonymous users. This can be done using the
:py:meth:`khoros.core.Khoros.BulkData.filter_anonymous` method.

By default, the method will remove all anonymous users and retain only data for logged-in users.
However, you can leverage the ``remove_registered`` Boolean parameter filter out logged-in users
instead and keep only the anonymous user data.

.. code-block:: python

   # The default parameters will remove anonymous user data
   filtered_data = khoros.bulk_data.filter_anonymous(bulk_data)

   # This will also remove anonymous user data
   filtered_data = khoros.bulk_data.filter_anonymous(bulk_data, remove_anonymous=True)

   # This will remove all logged-in user data
   filtered_data = khoros.bulk_data.filter_anonymous(bulk_data, remove_registered=True)

|

Filtering by Action
===================
If you are familiar with the `action.key events <https://developer.khoros.com/khoroscommunitydevdocs/reference/bulk-data-api#section-action-key-events>`_
then you can filter the data for only entries with that specific action using the
:py:meth:`khoros.core.Khoros.BulkData.filter_by_action` method, as demonstrated below.

.. code-block:: python

   # This will filter for only events relating to creating posts
   filtered_data = khoros.bulk_data.filter_by_action('messages.publish', bulk_data)

   # This will filter for only events relating to messages marked as an accepted solution
   filtered_data = khoros.bulk_data.filter_by_action('solutions.accept', bulk_data)

|

Counting Actions
================
If you just wish to count the number of times a specific event is found within your data
and do not need the raw data, then you can use the
:py:meth:`khoros.core.Khoros.BulkData.count_actions` method and supply the ``action.key``
value that you wish to count.

.. code-block:: python

   accepted_solution_count = khoros.bulk_data.count_actions(bulk_data, 'solutions.accept')

|

Counting Logins and Views
=========================
Two of the more common events (logins and views) have their own methods, which means you
won't need to remember their ``action.key`` values. These methods are
:py:meth:`khoros.core.Khoros.BulkData.count_logins` and
:py:meth:`khoros.core.Khoros.BulkData.count_views`, respectively, and they are demonstrated
below.

.. code-block:: python

   # This returns the number of logins as an integer
   num_logins = khoros.bulk_data.count_logins(bulk_data)

   # This returns the number of views as an integer
   num_views = khoros.bulk_data.count_views(bulk_data)

|
