Managing Node Settings
######################
You can manage the settings on any node (including categories, boards and grouphubs) using the :py:class:`khoros.core.Khoros.Settings` subclass, which leverages the :py:mod:`khoros.objects.settings` module. 

This guide demonstrates various ways that you can retrieve, define and update the node settings within your Khoros Communities environment. 

-----

|

Prerequisites
-------------
Throughout this guide we will assume that the Khoros core object has already been instantiated as ``khoros`` as shown below.

	.. code-block:: python
	
		 from khoros import Khoros
		 khoros = Khoros(helper='/Users/example/helper.yml')

-----

|

Retrieving node settings
------------------------
This section demonstrates how easy it is to retrieve a specific setting value from a node.

	.. caution:: These methods and functions assume you are querying a **board** by default. An additional parameter must be passed in order to query a **category** or **grouphub** node, as will be explained. 
	
|

Retrieving board settings
~~~~~~~~~~~~~~~~~~~~~~~~~
TBD

| 

Retrieving category settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TBD