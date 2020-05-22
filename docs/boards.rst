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
    * `Creating a New Forum`_
    * `Creating a New Blog`_

********
Overview
********
All of the board-specific functions reside within the :py:mod:`khoros.structures.boards`
module. However, they are also fully integrated into the :py:class:`khoros.core.Khoros`
object by way of the :py:class:`khoros.core.Khoros.Board` subclass and the associated
:py:class:`khoros.core.Khoros.boards` object class.

After :ref:`initializing the core object <introduction:Initializing a Khoros object instance>`,
the functions covered in the following sections can be leveraged for board-related operations.

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

======================== ======== ================================================================================================
Argument                 Type     Description
======================== ======== ================================================================================================
board_id*                string   The board ID
board_title*             string   The board title/name
discussion_style*        string   The type of discussion style
description              string   The description of the board
parent_category_id       string   The ID of the parent category (if applicable)
hidden                   boolean  Defines whether or not the new board should be hidden from lists and menus
allowed_labels           string   Type of labels permitted (``freeform-only``, ``predefined-only`` or ``freeform or pre-defined``)
use_freeform_labels      boolean  Indicates that only freeform labels should be permitted
use_predefined_labels    boolean  Indicates that only predefined labels should be permitted
predefined_labels        list     The list of predefined labels that are permitted
media_type               string   The media type associated with a contest (``image``, ``video`` or ``story`` meaning text)
blog_authors             list     The approved blog authors in a blog board as a list of user data dictionaries
blog_author_ids          list     A list of User IDs representing the approved blog authors in a blog board
blog_author_logins       list     A list of logins (i.e. usernames) representing the approved blog authors in a blog board
blog_comments_enabled    boolean  Indicates that comments should be enabled on blog posts within a blog board
blog_moderators          list     The designated moderators in a blog board as a list of user data dictionaries
blog_moderator_ids       list     A list of User IDs representing the blog moderators in a blog board
blog_moderator_logins    list     A list of logins (i.e. usernames) representing the moderators in a blog board
one_entry_per_contest    boolean  Indicates whether or not a user can only submit one entry to a single contest
one_kudo_per_contest     boolean  Indicates whether or not a user can vote only once per contest
posting_date_end         datetime The date/time a contest is closed to submissions
posting_date_start       datetime The date/time when the submission period for a contest begins
voting_date_end          datetime The date/time when the voting period for a contest ends
voting_date_start        datetime The date/time when the voting period for a contest begins
winner_announced_date    datetime The date/time the contest winner will be announced
full_response            boolean  Indicates whether the full, raw API response should be returned
return_id                boolean  Indicates whether the Board ID should be returned
return_url               boolean  Indicates whether the Board URL should be returned
return_api_url           boolean  Indicates whether the API URL (i.e. URI) of the board should be returned
return_http_code         boolean  Indicates whether the HTTP Code of the API request should be returned
return_status            boolean  Indicates whether the status of the API response should be returned
return_developer_message boolean  Indicates whether the Developer Response Message (if any) should be returned
======================== ======== ================================================================================================

.. note:: The fields labeled with an asterisk (*) are required.

Creating a New Forum
====================
To create a new forum, it is necessary to set the ``discussion_style`` argument equal
to ``forum`` when calling the ``boards.create()`` function. All other arguments, with the
exception of the ``board_id`` and ``board_title`` arguments, are optional.

.. code-block:: python

   >>> khoros.boards.create('my-new-forum', 'My New Forum', 'forum')

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
   >>> khoros.boards.create(board_id, board_title, discussion_style, blog_author_ids=authors, blog_moderator_ids=mods)

This example shows how to define authors and moderators using the user login values.

.. code-block:: python

   >>> authors = ['Ron Weasley', 'Neville Longbottom']
   >>> mods = ['Hermione Granger']
   >>> board_id, board_title, discussion_style = 'my-first-blog', 'My First Blog', 'blog'
   >>> khoros.boards.create(board_id, board_title, discussion_style, \
                            blog_author_logins=authors, blog_moderator_logins=mods)

Alternatively, if you happen to already have the fully formatted ``authors`` and ``moderators`` fields
for the API request, which would be a list of dictionaries containing user data, then they can be used
instead via the ``blog_authors`` and ``blog_moderators`` function arguments, as demonstrated below.

.. todo:: Finish this tutorial