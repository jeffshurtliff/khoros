# Python SDK for Khoros Communities
The **khoros** library acts as a Python software development kit (SDK) to administer and manage 
[Khoros Communities](https://khoros.com/platform/communities) (formerly Lithium)  online community platforms.

<table>
    <tr>
        <td>Latest Stable Release</td>
        <td>
            <a href='https://pypi.org/project/khoros/'>
                <img alt="PyPI" src="https://img.shields.io/pypi/v/khoros">
            </a>
        </td>
    </tr>
    <tr>
        <td>Latest Beta/RC Release</td>
        <td>
            <a href='https://pypi.org/project/khoros/#history'>
                <img alt="PyPI" src="https://img.shields.io/badge/pypi-5.2.0rc1-blue">
            </a>
        </td>
    </tr>
    <tr>
        <td>Build Status</td>
        <td>
            <a href="https://github.com/jeffshurtliff/khoros/blob/master/.github/workflows/pythonpackage.yml">
                <img alt="GitHub Workflow Status" 
                src="https://img.shields.io/github/actions/workflow/status/jeffshurtliff/khoros/pythonpackage.yml?branch=master">
            </a>
        </td>
    </tr>
    <tr>
        <td>Supported Versions</td>
        <td>
            <a href='https://pypi.org/project/khoros/'>
                <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/khoros">
            </a>
        </td>
    </tr>
    <tr>
        <td>Code Coverage</td>
        <td>
            <a href="https://codecov.io/gh/jeffshurtliff/khoros">
                <img src="https://codecov.io/gh/jeffshurtliff/khoros/branch/master/graph/badge.svg" />
            </a>
        </td>
    </tr>
    <tr>
        <td>CodeFactor Grade</td>
        <td>
            <a href="https://lgtm.com/projects/g/jeffshurtliff/khoros">
            <img alt="CodeFactor Grade" src="https://img.shields.io/codefactor/grade/github/jeffshurtliff/khoros">
            </a>
        </td>
    </tr>
    <tr>
        <td>Documentation</td>
        <td>
            <a href='https://khoros.readthedocs.io/en/latest/?badge=latest'>
                <img src='https://readthedocs.org/projects/khoros/badge/?version=latest' alt='Documentation Status' /><br />
                <img src="https://raw.githubusercontent.com/jeffshurtliff/khoros/master/docs/_static/interrogate_badge.svg">
            </a>
        </td>
    </tr>
    <tr>
        <td>Security Audits</td>
        <td>
            <a href="https://github.com/marketplace/actions/python-security-check-using-bandit">
                <img alt="Bandit" src="https://img.shields.io/badge/security-bandit-yellow.svg">
            </a><br />
            <a href="https://github.com/marketplace/actions/pycharm-python-security-scanner">
                <img alt="PyCharm Security Scanner" src="https://img.shields.io/badge/security-pycharm%20security%20scanner-green">
            </a>
        </td>
    </tr>
    <tr>
        <td>License</td>
        <td>
            <a href="https://github.com/jeffshurtliff/khoros/blob/master/LICENSE">
                <img alt="License (GitHub)" src="https://img.shields.io/github/license/jeffshurtliff/khoros">
            </a>
        </td>
    </tr>
    <tr>
        <td style="vertical-align: top;">Issues</td>
        <td>
            <a href="https://github.com/jeffshurtliff/khoros/issues">
                <img style="margin-bottom:5px;" alt="GitHub open issues" src="https://img.shields.io/github/issues-raw/jeffshurtliff/khoros"><br />
            </a>
            <a href="https://github.com/jeffshurtliff/khoros/issues">
                <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed-raw/jeffshurtliff/khoros">
            </a>
        </td>
    </tr>
    <tr>
        <td style="vertical-align: top;">Pull Requests</td>
        <td>
            <a href="https://github.com/jeffshurtliff/khoros/pulls">
                <img style="margin-bottom:5px;" alt="GitHub pull open requests" src="https://img.shields.io/github/issues-pr-raw/jeffshurtliff/khoros"><br />
            </a>
            <a href="https://github.com/jeffshurtliff/khoros/pulls">
                <img alt="GitHub closed pull requests" src="https://img.shields.io/github/issues-pr-closed-raw/jeffshurtliff/khoros">
            </a>
        </td>
    </tr>
</table>

## Installation
The package can be installed via pip using the syntax below.

```sh
pip install khoros --upgrade
```

You may also clone the repository and install from source using below.

```sh
git clone git://github.com/jeffshurtliff/khoros.git
cd khoros/
python setup.py install
```

## Change Log
The change log can be found in the [documentation](https://khoros.readthedocs.io/en/latest/changelog.html).

## Usage
This section provides basic usage instructions for the package.

### Importing the package
Rather than importing the base package, it is recommended that you import the primary `Khoros` class using the syntax
below.

```python
from khoros import Khoros
```

This recommendation is because the best practice is to use the name `khoros` when naming your object instance.

### Initializing a Khoros object instance
The primary `Khoros` object serves many purposes, the most important being to establish a connection to the Khoros
Community environment with which you intend to interact. As such, when initializing an instance of the `Khoros` object,
you will need to pass it the community URL, the credentials it will use and related information so that the connection
can be established.

The `Khoros` object can be initiated in two different ways:
* Passing the information directly into the object
* Leveraging a "helper" configuration file

#### Passing the information directly into the object
The community and connection information can be passed directly into the `Khoros` object when initializing it, as
demonstrated in the example below.

```python
# Using Session Key authentication
khoros = Khoros(
    community_url='https://community.example.com', 
    session_auth={'username': USERNAME, 'password': PASSWD}
)

# Using LithiumSSO Token authentication
khoros = Khoros(
    community_url='https://community.example.com', 
    sso={'sso.authentication_token': LITHIUM_SSO_TOKEN}
)
```

Alternatively, configuration settings can be passed at once using the `options` argument in the `Khoros` class, as 
shown below.

```python
my_settings = {
    'community_url': 'https://community.example.com',
    'community_name': 'mycommunity',
    'auth_type': 'session_auth',
    'session_auth': {
        'username': USERNAME,
        'password': PASSWD
    }
}
```

#### Leveraging a "helper" configuration file
As an alternative to passing the connection information to the `Khoros` class in the ways demonstrated above, a
"helper" configuration file in `yaml` or `json` format can be leveraged instead and passed to the `Khoros` class
when initializing the object.

This is an example of how the configuration file would be written:

```yaml
# Helper configuration file for the khoros package

# Define how to obtain the connection information
connection:
    community_url: https://community.example.com/
    tenant_id: example12345

    # Define the default authentication type to use
    default_auth_type: session_auth

    # Define the OAuth 2.0 credentials
    oauth2:
        client_id: FLFeNYob7XXXXXXXXXXXXXXXXXXXXZcWQEQHR5T6bo=
        client_secret: 1n0AIXXXXXXXXXXXXXXXXXXXX1udOtNaYnfJCeOszYw=
        redirect_url: http://redirect.community.example.com/getAccessToken

    # Define the session key authorization information
    session_auth:
        username: serviceaccount
        password: Ch@ng3ME!

    # Bulk Data API connection information
    bulk_data:
        community_id: example.prod
        client_id: ay0CXXXXXXXXXX/XXXX+XXXXXXXXXXXXX/XXXXX4KhQ=
        token: 2f25XXXXXXXXXXXXXXXXXXXXXXXXXa10dec04068
        europe: no

# Define the preferred format for API responses
prefer_json: yes
```

The file can then be referenced using the `helper` argument when initializing the object instance, as shown below.

```python
HELPER_FILE = "/path/to/helper.yml"
khoros = Khoros(helper=HELPER_FILE)
```

#### Utilizing environment variables
This third method of initializing a Khoros object instance is definitely the easiest, as it allows you to call
upon the `Khoros` class without passing any arguments, as shown below.

```python
from khoros import Khoros
khoros = Khoros()
```

This is accomplished by defining environment variables within your Operating System, either through the
[graphical UI](https://www.techjunkie.com/environment-variables-windows-10/), the command-line or within the Python
IDE using the `os` module and
[adding entries](https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5) to the
`os.environ` dictionary, as shown below.

```python
import os
os.environ['KHOROS_URL'] = 'https://community.example.com'
```

| Environment Variable      | Description                                                                                                                                                | Example                                                |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| KHOROS_URL                | The base URL of the environment                                                                                                                            | `https://community.example.com`                        |
| KHOROS_TENANT_ID          | The [Tenant ID](https://developer.khoros.com/khoroscommunitydevdocs/docs/oauth-authorization-grant) associated with your environment                       | `abcde12345`                                           |
| KHOROS_DEFAULT_AUTH       | The default authentication method you wish to use                                                                                                          | `session_auth`                                         |
| KHOROS_OAUTH_ID           | The Client ID utilized by the [OAuth 2.0](https://developer.khoros.com/khoroscommunitydevdocs/docs/oauth-authorization-grant) authorization grant flow     | `FXXXXXXb7owXXXXXXo+jFlPXXXXXXjZcWQXXXXXX6bo=`         |
| KHOROS_OAUTH_SECRET       | The Client Secret utilized by the [OAuth 2.0](https://developer.khoros.com/khoroscommunitydevdocs/docs/oauth-authorization-grant) authorization grant flow | `1XXXXXX+/kZXXXXXXZZ9u1B5+1uXXXXXXfJCeOszYw=`          |
| KHOROS_OAUTH_REDIRECT_URL | The Redirect URL utilized by the [OAuth 2.0](https://developer.khoros.com/khoroscommunitydevdocs/docs/oauth-authorization-grant) authorization grant flow  | `http://redirect.community.example.com/getAccessToken` |
| KHOROS_SESSION_USER       | The username to use with [Session Key](https://developer.khoros.com/khoroscommunitydevdocs/docs/session-key) authentication                                | `apiuser`                                              |
| KHOROS_SESSION_PW         | The password to use with [Session Key](https://developer.khoros.com/khoroscommunitydevdocs/docs/session-key) authentication                                | `Ch@ng3M3!`                                            |
| KHOROS_PREFER_JSON        | Boolean string indicating if JSON responses are preferred                                                                                                  | `True`                                                 |
| KHOROS_LIQL_PRETTY        | Boolean string indicating if reader-friendly formatting should be used                                                                                     | `False`                                                |
| KHOROS_LIQL_TRACK_LSI     | Boolean string indicating if queries should be captured in Community Analytics search reports                                                              | `False`                                                |
| KHOROS_LIQL_ALWAYS_OK     | Boolean string indicating if all responses should return a `200 OK` status code                                                                            | `False`                                                |
| KHOROS_TRANSLATE_ERRORS   | Boolean string indicating if errors in API responses should be made more relevant where possible                                                           | `True`                                                 |

If you are leveraging this library on a macOS or Linux operating system (e.g. Ubuntu Server) then you can simply
add the environment variables you wish to define to either the `/etc/environment` file if you wish to apply
them to all users, or to your user's `~/.bashrc` file for them to only apply to your user.

```shell script
# Define environment variables for Khoros
KHOROS_URL='https://community.example.com'
```

>**Note:**
>You will generally need to log out and log back in for the changes to take effect.

If you are leveraging this library on a Windows operating system (e.g. Windows 10) then you can add environment
variables for your user via the Command Prompt (i.e. `cmd.exe`) or  PowerShell.

>**Note:**
>Using either of these two methods, you can add the environment variables using an interactive terminal
>window or using a batch/script file.  (Files should use the `.bat` or `.cmd` extension for the
>Command Prompt and `.ps1` for PowerShell.)

**Command Prompt**

```batch
@echo off
echo Defining the KHOROS_URL environment variable...
setx KHOROS_URL https://community.example.com
echo.
```

**PowerShell**

```powershell
"Defining the KHOROS_URL environment variable..."
[Environment]::SetEnvironmentVariable("KHOROS_URL", "https://community.example.com/", "User")
```

### Interacting with the Community APIs
Once the `Khoros` object instance has been initialized, it can be leveraged to interact with a Khoros Community
environment in many ways, which is fully documented in the official
[documentation](https://khoros.readthedocs.io/en/latest/). The example below demonstrates how a search can be
performed using LiQL to return information from the environment in JSON format.

```python
response_json = khoros.search(
    select_fields=('id', 'view_href'),
    from_source='messages',
    where_filter=('style', 'tkb'),
    order_by='last_post_time',
    limit=5
)
```

## Documentation
The documentation is located here: [https://khoros.readthedocs.io/en/latest/](https://khoros.readthedocs.io/en/latest/)

## License
[MIT License](https://github.com/jeffshurtliff/khoros/blob/master/LICENSE)

## Reporting Issues
Issues can be reported within the [GitHub repository](https://github.com/jeffshurtliff/khoros/issues).

## Roadmap
Upcoming improvements to the library can be found in the following locations: 
 - [2020 Roadmap on GitHub](https://github.com/jeffshurtliff/khoros/projects/1)
 - [2021 Roadmap on GitHub](https://github.com/jeffshurtliff/khoros/projects/2)
 - [2022 Roadmap on GitHub](https://github.com/jeffshurtliff/khoros/projects/3)

## Additional Resources
Additional resources for leveraging the Community APIs can be found in the official
[Khoros Developer Documentation](https://developer.khoros.com/khoroscommunitydevdocs).

## Donations
If you would like to donate to this project then you can do so using [this PayPal link](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=XDZ8M6UV6EFK6&item_name=Khoros+Python+API&currency_code=USD).

## Disclaimer
This package is considered unofficial and is in no way endorsed or supported by [Khoros, LLC](https://www.khoros.com).
