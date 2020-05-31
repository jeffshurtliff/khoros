###################
Working with Boards
###################
Boards are the primary residence of all content in a Khoros Community environment,
and they can be created, queried, manipulated and even deleted using the Khoros
Community APIs.

This section addresses how the Khoros Community Python library leverages these
APIs to harness these boards.

* `Overview`_
* `Creating a New Board`_
    * `Return Options`_
        * `Simple Boolean Response (Default)`_
        * `Full API Response`_
        * `Return the Board ID`_
        * `Return the Board URL`_
        * `Return the Board API URL`_
        * `Return the API response HTTP Code`_
        * `Return the API response status`_
        * `Return Any Error Messages`_
        * `Return Multiple Types`_
    * `Creating a New Forum`_
    * `Creating a New Blog`_
    * `Creating a New Tribal Knowledge Base (TKB)`_
    * `Creating a New Q&A Board`_
    * `Creating a New Idea Exchange`_
    * `Creating a New Contest`_
    * `Optional Configuration Items`_
        * `Adding a Description`_
        * `Defining the Parent Category`_
        * `Creating a Hidden Board`_
        * `Configuring Label Settings`_
* `Retrieving a Board ID`_

|

********
Overview
********
All of the board-specific functions reside within the :py:mod:`khoros.structures.boards`
module. However, they are also fully integrated into the :py:class:`khoros.core.Khoros`
object by way of the :py:class:`khoros.core.Khoros.Board` subclass and the associated
:py:class:`khoros.core.Khoros.boards` object class.

After :ref:`initializing the core object <introduction:Initializing a Khoros object instance>`,
the functions covered in the following sections can be leveraged for board-related operations.

.. caution:: This tutorial assumes that the core object has been initialized as ``khoros`` per
             the naming convention best practices defined on the :doc:`introduction` page.

:doc:`Return to Top <boards>`

********************
Creating a New Board
********************
A new board can be created using the ``boards.create()`` function via the initiated core object,
as demonstrated below.

.. code-block:: python

   >>> khoros.boards.create('my-board', 'My Board', 'forum', return_status=True)
   'success'

The table below lists the arguments that can/must be used in the function, which leverages
the :py:func:`khoros.structures.boards.create` function.

===================== ======== ====================================================================================================
Argument              Type     Description
===================== ======== ====================================================================================================
board_id*             string   The board ID
board_title*          string   The board title/name
discussion_style*     string   The type of discussion style (e.g. ``blog``, ``contest``, ``forum``, ``idea``, ``qanda`` or ``tkb``)
description           string   The description of the board
parent_category_id    string   The ID of the parent category (if applicable)
hidden                boolean  Defines whether or not the new board should be hidden from lists and menus
allowed_labels        string   Type of labels permitted (``freeform-only``, ``predefined-only`` or ``freeform or pre-defined``)
use_freeform_labels   boolean  Indicates that only freeform labels should be permitted
use_predefined_labels boolean  Indicates that only predefined labels should be permitted
predefined_labels     list     The list of predefined labels that are permitted
media_type            string   The media type associated with a contest (``image``, ``video`` or ``story`` meaning text)
blog_authors          list     The approved blog authors in a blog board as a list of user data dictionaries
blog_author_ids       list     A list of User IDs representing the approved blog authors in a blog board
blog_author_logins    list     A list of logins (i.e. usernames) representing the approved blog authors in a blog board
blog_comments_enabled boolean  Indicates that comments should be enabled on blog posts within a blog board
blog_moderators       list     The designated moderators in a blog board as a list of user data dictionaries
blog_moderator_ids    list     A list of User IDs representing the blog moderators in a blog board
blog_moderator_logins list     A list of logins (i.e. usernames) representing the moderators in a blog board
one_entry_per_contest boolean  Indicates whether or not a user can only submit one entry to a single contest
one_kudo_per_contest  boolean  Indicates whether or not a user can vote only once per contest
posting_date_end      datetime The date/time a contest is closed to submissions
posting_date_start    datetime The date/time when the submission period for a contest begins
voting_date_end       datetime The date/time when the voting period for a contest ends
voting_date_start     datetime The date/time when the voting period for a contest begins
winner_announced_date datetime The date/time the contest winner will be announced
full_response         boolean  Indicates whether the full, raw API response should be returned
return_id             boolean  Indicates whether the Board ID should be returned
return_url            boolean  Indicates whether the Board URL should be returned
return_api_url        boolean  Indicates whether the API URL (i.e. URI) of the board should be returned
return_http_code      boolean  Indicates whether the HTTP Code of the API response should be returned
return_status         boolean  Indicates whether the status of the API response should be returned
return_error_messages boolean  Indicates whether the Developer Response Message (if any) should be returned
===================== ======== ====================================================================================================

.. note:: The fields labeled with an asterisk (*) are required.

:doc:`Return to Top <boards>`

Return Options
==============
There are multiple ways to return data when creating a board, which can be explicitly
defined using one or more of the following function arguments:

* :ref:`full_response <boards:Full API Response>`
* :ref:`return_id <boards:Return the Board ID>`
* :ref:`return_url <boards:Return the Board URL>`
* :ref:`return_api_url <boards:Return the Board API URL>`
* :ref:`return_http_code <boards:Return the API Response HTTP Code>`
* :ref:`return_status <boards:Return the API Response Status>`
* :ref:`return_error_messages <boards:Return Any Error Messages>`

These arguments are explained in more detail within the sub-sections below.

:doc:`Return to Top <boards>`

|

Simple Boolean Response (Default)
---------------------------------
Unless explicitly defined, the function will return a simple Boolean response
(i.e. ``True`` or ``False``) indicating whether or not the operation was successful.

.. code-block:: python

   >>> def create_and_check():
   ...     successful = khoros.boards.create('my-new-forum', 'My New Forum', 'forum')
   ...     result = "It worked!" if successful else "It failed!"
   ...     print(result)
   ...

   >>> create_and_check()
   'It worked!'

:doc:`Return to Top <boards>`

|

Full API Response
-----------------
If you'd rather return the full, raw response from the API request in order to parse
it later at your convenience, then this can be done by setting the ``full_response``
argument to ``True`` in the function call as shown below.

.. code-block:: python

   >>> response = khoros.boards.create('my-new-forum', 'My New Forum', 'forum', full_response=True)
   >>> if response.status_code != 404:
   ...     response = response.json()
   ...     print(response['status'])
   'success'

:doc:`Return to Top <boards>`

|

Return the Board ID
-------------------
If it makes sense for you to return the ID of the board you just created then
you can do so by defining the ``return_id`` argument as ``True`` as seen below.

.. code-block:: python

   >>> forums_to_create = [('first-board', 'My First Board'), ('second-board', 'My Second Board')]
   >>> for forum in forums_to_create:
   ...     board_id, board_title = forum
   ...     forum_id = khoros.boards.create(board_id, board_title, 'forum', return_id=True)
   ...     print("Forum Created:", forum_id)
   'Forum Created: first-board'
   'Forum Created: second-board'

:doc:`Return to Top <boards>`

|

Return the Board URL
--------------------
Very likely the most popular return option for this function, defining the ``return_url``
argument as ``True`` will return the URL of the newly created board, as shown below.

.. code-block:: python

   >>> khoros.boards.create('python-lovers', 'The Python Lovers Blog', \
   ... 'blog', return_url=True)
   'https://stage.example.com/t5/The-Python-Lovers-Blog/bg-p/python-lovers'

:doc:`Return to Top <boards>`

|

Return the Board API URL
------------------------
If additional API calls will be immediately performed following the creation of a board,
it may be useful to return the API URL (i.e. URI) for the new board by defining the
``return_api_url`` argument as ``True``, as shown below.

.. code-block:: python

   >>> khoros.boards.create('python-lovers', 'The Python Lovers Blog', \
   ... 'blog', return_api_url=True)
   '/boards/python-lovers'

:doc:`Return to Top <boards>`

|

Return the API Response HTTP Code
---------------------------------
Another potentially useful return option is to define the ``return_http_code``
argument as ``True``, which will return the
`HTTP status code <https://en.wikipedia.org/wiki/List_of_HTTP_status_codes>`_
for the API response, as demonstrated below.

.. code-block:: python

   >>> khoros.boards.create('python-lovers', 'The Python Lovers Blog', \
   ... 'blog', return_http_code=True)
   200

:doc:`Return to Top <boards>`

|

Return the API Response Status
------------------------------
Alternatively, it is possible to return the status of the API response (as defined
by Khoros in the JSON response) by defining the ``return_status`` argument as
``True``, as shown below.

.. code-block:: python

   >>> khoros.boards.create('my-first-blog', 'My First Blog', 'blog', \
   ... return_status=True)
   'success'

   >>> khoros.boards.create('my-first-blog', 'My First Blog', 'blog', \
   ... return_status=True)
   'error'

:doc:`Return to Top <boards>`

|

Return Any Error Messages
-------------------------
If you want to ensure that you see any error messages when applicable but don't want to
return the full API response, you can define the ``return_error_messages`` argument as
``True``, as shown below.

.. code-block:: python

   >>> khoros.boards.create('my-first-blog', 'My First Blog', \
   ... 'blog', return_error_messages=True)
   "An object of type blog-board already exists with the 'id' property value 'my-first-blog'"

This argument captures both the ``message`` value and the occasionally populated
``developer_message`` value. If one of the values is blank or if they are exactly the same, such
as in the example above, then only one of the values will be displayed. Otherwise, if both values
are defined and do not match then they will be returned in the ``{message} - {developer_message}``
format.  (i.e. The two values will be separated by spaces and a hyphen.)

If you wish to return both fields regardless of their values then you can define the optional
``split_errors`` argument as ``True`` as well to return a tuple containing both values, as shown
below.

.. code-block:: python

   >>> khoros.boards.create('my-first-blog', 'My First Blog', 'blog', \
   ... return_error_messages=True, split_errors=True)
   ("An object of type blog-board already exists with the 'id' property value 'my-first-blog'", "An object of type blog-board already exists with the 'id' property value 'my-first-blog'")

:doc:`Return to Top <boards>`

|

Return Multiple Types
---------------------
You are not restricted to choosing only one of the return options. You can enable as many options as needed and if
multiple types are detected by the function then they will be returned as a tuple with those values, as demonstrated
in the example below.

.. code-block:: python

   >>> response = khoros.boards.create('my-first-blog', 'My First Blog', 'blog', \
   ... return_http_code=True, return_status=True, return_error_messages=True)

   >>> if response[1] == 'success':
   ...     print(f"The board creation was successful with the HTTP code {response[0]}.")
   ... else:
   ...     print(f"The board creation failed with the following error:\n{response[2]}")
   ...
   The board creation failed with the following error:
   An object of type blog-board already exists with the 'id' property value 'my-first-blog'

.. note:: The tuple will return the values in the order they are listed as function arguments.

:doc:`Return to Top <boards>`

|

Creating a New Forum
====================
To create a new forum, it is necessary to set the ``discussion_style`` argument equal
to ``forum`` when calling the ``boards.create()`` function. All other arguments, with the
exception of the ``board_id`` and ``board_title`` arguments, are optional.

.. code-block:: python

   >>> khoros.boards.create('my-new-forum', 'My New Forum', 'forum')

:doc:`Return to Top <boards>`

|

Creating a New Blog
===================
To create a new forum, it is necessary to set the ``discussion_style`` argument equal
to ``blog`` when calling the ``boards.create()`` function, in addition to defining the
``board_id`` and ``board_title``.

Blog boards also have the option of explicitly defining approved blog authors and/or
designated blog moderators at the time of the board creation. The easiest way of doing
this is by supplying a list of User IDs (via the ``blog_author_ids`` and ``blog_moderator_ids``
arguments) or by supplying a list of logins (i.e. usernames) via the ``blog_author_logins``
and ``blog_moderator_logins`` arguments.  These options are demonstrated below.

This example shows how to define authors and moderators using the User ID values.

.. code-block:: python

   >>> authors = ['23', '44', '67']
   >>> mods = ['5', '19']
   >>> board_id, board_title, discussion_style = 'my-first-blog', 'My First Blog', 'blog'
   >>> khoros.boards.create(board_id, board_title, discussion_style, \
                            blog_author_ids=authors, blog_moderator_ids=mods)

This example shows how to define authors and moderators using the user login values.

.. code-block:: python

   >>> authors = ['Ron Weasley', 'Neville Longbottom']
   >>> mods = ['Hermione Granger']
   >>> board_id, board_title, discussion_style = 'my-first-blog', 'My First Blog', 'blog'
   >>> khoros.boards.create(board_id, board_title, discussion_style, \
   ...                      blog_author_logins=authors, blog_moderator_logins=mods)

Alternatively, if you happen to already have the fully formatted ``authors`` and ``moderators`` fields
for the API request, which would be a list of dictionaries containing user data, then they can be used
instead via the ``blog_authors`` and ``blog_moderators`` function arguments, as demonstrated below.

.. code-block:: python

   >>> authors = [{"id": "45"}, {"id": "57"}]
   >>> mods = [{"id": "12"}]
   >>> board_id, board_title, discussion_style = 'my-first-blog', 'My First Blog', 'blog'
   >>> khoros.boards.create(board_id, board_title, discussion_style, \
   ...                      blog_authors=authors, blog_moderators=mods)

:doc:`Return to Top <boards>`

|

Creating a New Tribal Knowledge Base (TKB)
==========================================
Creating a new Tribal Knowledge Base, or TKB, is very similar to creating a
forum, except that the ``discussion_style`` argument will be defined as ``tkb``
as shown in the example below.

.. code-block:: python

   >>> khoros.boards.create('product-knowledge-base', 'Product Knowledge Base', \
   ...                      'tkb', return_status=True)
   'success'

:doc:`Return to Top <boards>`

|

Creating a New Q&A Board
========================
Creating a new Q&A board is also similar to creatinga forum, except that the
``discussion_style`` argument will be defined as ``qanda`` sa shown below.

.. code-block:: python

   >>> khoros.boards.create('product-questions', 'Product Questions', \
   ...                      'qanda', return_status=True)
   'success'

:doc:`Return to Top <boards>`

|

Creating a New Idea Exchange
============================
Idea Exchange boards (used for
`ideation <https://community.khoros.com/t5/Ideas/Fostering-a-flourishing-ideation-process/ta-p/404636>`_)
can be created by defining the ``discussion_style`` argument as ``idea``, as shown below.

.. code-block:: python

   >>> khoros.boards.create('product-idea-exchange', 'Product Idea Exchange', \
   ...                      'idea', one_entry_per_contest=False, \
   ...                      one_kudo_per_contest=True, return_status=True)
   'success'

:doc:`Return to Top <boards>`

|

Creating a New Contest
======================
Contest boards can be created by defining the ``discussion_style`` argument as
``contest``. Contests also have several unique optional arguments that can be
used, which are listed in the :ref:`table <boards:Creating a New Board>` earlier
in this tutorial and again below.

===================== ======== =========================================================================================
Argument              Type     Description
===================== ======== =========================================================================================
media_type            string   The media type associated with a contest (``image``, ``video`` or ``story`` meaning text)
one_entry_per_contest boolean  Indicates whether or not a user can only submit one entry to a single contest
one_kudo_per_contest  boolean  Indicates whether or not a user can vote only once per contest
posting_date_end      datetime The date/time a contest is closed to submissions
posting_date_start    datetime The date/time when the submission period for a contest begins
voting_date_end       datetime The date/time when the voting period for a contest ends
voting_date_start     datetime The date/time when the voting period for a contest begins
winner_announced_date datetime The date/time the contest winner will be announced
===================== ======== =========================================================================================

A function call using some of these arguments is shown below.

.. code-block:: python

   >>> khoros.boards.create('product-innovation-contest', 'Product Innovation Contest', \
   ...                      'contest', one_entry_per_contest=False, \
   ...                      one_kudo_per_contest=True, media_type='story', return_status=True)
   'success'

:doc:`Return to Top <boards>`

|

Optional Configuration Items
============================
There are several other optional arguments that may also be passed in the function call
to define other elements of the new board, which are addressed in the sub-sections below.

:doc:`Return to Top <boards>`

|

Adding a Description
--------------------
As it is an SEO best practice to include a description when creating a new board, it is
recommended that you define the optional ``description`` argument whenever using the
:py:func:`khoros.structures.boards.create` function, as demonstrated below.

.. code-block:: python

   >>> khoros.boards.create('upcoming-events', 'Upcoming Events', 'blog', \
   ...                      'Get the details on our upcoming events and product releases.')
   True

.. note:: As the ``description`` argument immediately follows the three required arguments
          in the function call, it is not necessary to define it using a keyword argument.
          (e.g. ``description='Get the details...'``)

:doc:`Return to Top <boards>`

|

Defining the Parent Category
----------------------------
By default, a new board will be created at the top-most level of the community environment.
However, if you intend to create the board below a specific category then this can
easily be done by supplying the ID of said category via the ``parent_category_id`` argument,
as demonstrated below.

.. code-block:: python

   >>> khoros.boards.create('upcoming-events', 'Upcoming Events', 'blog', \
   ...                      'Get the details on our upcoming events and product releases.', \
   ...                      parent_category_id='products')
   True

:doc:`Return to Top <boards>`

|

Creating a Hidden Board
-----------------------
If you do not want your new board to appear in lists or menus then you can flag it as a
"hidden" board by defining the ``hidden`` argument as ``True`` in the function call,
as shown below.

.. code-block:: python

   >>> khoros.boards.create('tkb-archive', 'Archived TKB Articles', 'tkb', hidden=True)
   True

:doc:`Return to Top <boards>`

|

Configuring Label Settings
--------------------------
While creating a board, you can configure the label settings up front via the function
call if desired, rather than configuring them later in the Community Admin UI or via
separate API requests.

The first setting you can configure is whether or not the board will allow **freeform**
labels (i.e. where users can create their own labels), **predefined** labels (i.e.
where community managers define the labels and users can only select them) or both.

There are two ways to do this:

* The first method is to define the ``allowed_labels`` argument as either ``freeform-only``,
  ``predefined-only`` or ``freeform or pre-defined``.

.. code-block:: python

   >>> khoros.boards.create('product-discussions', 'Product Discussions', 'forum', \
   ...                      allowed_labels='freeform-only')
   True

* The second method is to define the Boolean arguments ``use_freeform_labels`` and/or
  ``use_predefined_labels`` as ``True``.

.. code-block:: python

   >>> khoros.boards.create('product-discussions', 'Product Discussions', 'forum', \
   ...                      use_freeform_labels=True)
   True

.. note:: Defining both ``use_freeform_labels`` and ``use_predefined_labels`` as ``True``
          is the equivalent of defining the ``allowed_labels`` argument as
          ``freeform or pre-defined``.

:doc:`Return to Top <boards>`

|

*********************
Retrieving a Board ID
*********************
The majority of Khoros Community API calls--and therefore the majority of functions and methods in
this library--relating to boards require a board ID to be provided.  As such, it will often be
necessary for you to quickly retrieve a board ID, which is easy to do via the
:py:func:`khoros.core.Khoros.Board.get_board_id` function.

This function requires only the URL of the board and can be called from within the core object
(i.e. :py:class:`khoros.core.Khoros`) using the :py:meth:`khoros.core.Khoros.boards.get_board_id`
method call as demonstrated below.

.. code-block:: python

   >>> from khoros import Khoros
   >>> khoros = Khoros(helper='~/helper.yml')
   >>> khoros.boards.get_board_id('https://community.example.com/t5/example-board/tkb-p/example-board')
   'example-board'

   >>>

.. note:: This function will work with boards for all discussion styles.

The retrieved board ID can then be used in other functions and methods to perform any
necessary tasks.
