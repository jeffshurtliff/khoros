##############################
Performing Community API Calls
##############################
Using the Khoros Python API to perform Community API calls is easier than doing
so manually with the *requests* library for several reasons, including:

* It is unnecessary to pass the entire URL as the base URL is stored in the :py:class:`khoros.core.Khoros` object. This means the relative URL passed in functions is generallu the same that would be passed to the *rest* or *restadmin* FreeMarker directives in components, macros or endpoints. 
* The authorization token (e.g. `li-api-session-key`) is automatically included in the request header for all API calls. 
* Errors and exceptions are more intuitive with Khoros-specific messages.

There are three types of API calls 