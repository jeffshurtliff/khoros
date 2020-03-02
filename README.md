# Khoros Community Python Library
The  **khoros**  library acts as a Python software development kit (SDK) to administer and manage 
[Khoros Community](https://developer.khoros.com/khoroscommunitydevdocs) (formerly Lithium)  online community platforms.

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
        <td>Build Status</td>
        <td>
            <a href="https://github.com/jeffshurtliff/khoros/blob/master/.github/workflows/pythonpackage.yml">
                <img alt="GitHub Workflow Status" 
                src="https://img.shields.io/github/workflow/status/jeffshurtliff/khoros/Python package">
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
        <td>Documentation</td>
        <td>
            <a href='https://khoros.readthedocs.io/en/latest/?badge=latest'>
                <img src='https://readthedocs.org/projects/khoros/badge/?version=latest' alt='Documentation Status' />
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
pip install khoros
```

You may also clone the repository and install from source using below.

```sh
git clone git://github.com/jeffshurtliff/khoros.git
cd khoros/
python setup.py install
```

## Change Log
Coming in the next version

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
khoros = Khoros(community_url='https://community.example.com', session_auth={'username': USERNAME, 'password': PASSWD})
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

# Define the preferred format for API responses
prefer_json: yes
```

The file can then be referenced using the `helper` argument when initializing the object instance, as shown below.

```python
HELPER_FILE = "/path/to/helper.yml"
khoros = Khoros(helper=HELPER_FILE)
```

### Interacting with the Community APIs
Once the `Khoros` object instance has been initialized, it can be leveraged to interact with a Khoros Community
environment in many ways, which will be fully documented shortly in the 
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
[MIT License](https://github.com/jeffshurtliff/khorosjx/blob/master/LICENSE)

## Reporting Issues
Issues can be reported within the [GitHub repository](https://github.com/jeffshurtliff/khoros/issues).

## Disclaimer
This package is considered unofficial and is in no way endorsed or supported by [Khoros](https://www.khoros.com).
