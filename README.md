# grafana-client [![Github Actions Test](https://github.com/panodata/grafana-client/workflows/Test/badge.svg)](https://github.com/panodata/grafana-client/actions?query=workflow%3ATest) [![GitHub license](https://img.shields.io/github/license/panodata/grafana-client.svg?style=flat-square)](https://github.com/panodata/grafana-client/blob/master/LICENSE)  [![Codecov](https://img.shields.io/codecov/c/gh/panodata/grafana-client.svg?style=flat-square)](https://codecov.io/gh/panodata/grafana-client/)

[![PyPI](https://img.shields.io/pypi/v/grafana-client.svg?style=flat-square)](https://pypi.org/project/grafana-api/) [![Conda](https://img.shields.io/conda/v/panodata/grafana-client.svg?style=flat-square)](https://anaconda.org/panodata/grafana-client)

## What is this library for?

Yet another Grafana API library for Python. Support Python 3 only.

## Requirements

You need Python 3 and only the `requests` library installed.

## History

The library was originally conceived by Andrew Prokhorenkov at https://github.com/m0nhawk/grafana_api.
Thank you very much for your efforts!

## Quick start

Install the pip package:

```
pip install -U grafana-client
```

And then connect to your Grafana API endpoint:

```python
from grafana_client.grafana_face import GrafanaFace

grafana = GrafanaFace(auth='abcde....', host='api.my-grafana-host.com')

# Create user
user = grafana.admin.create_user({"name": "User", "email": "user@domain.com", "login": "user", "password": "userpassword", "OrgId": 1})

# Change user password
user = grafana.admin.change_user_password(2, "newpassword")

# Search dashboards based on tag
grafana.search.search_dashboards(tag='applications')

# Find a user by email
user = grafana.users.find_user('test@test.com')

# Add user to team 2
grafana.teams.add_team_member(2, user["id"])

# Create or update a dashboard
grafana.dashboard.update_dashboard(dashboard={'dashboard': {...}, 'folderId': 0, 'overwrite': True})

# Delete a dashboard by UID
grafana.dashboard.delete_dashboard(dashboard_uid='abcdefgh')

# Create organization
grafana.organization.create_organization({"name":"new_organization"})
```


## Authentication

There are two ways to autheticate to grafana api. Either use api token or basic auth.

To use admin API you need to use basic auth [as stated here](https://grafana.com/docs/grafana/latest/http_api/admin/)

```python
# Use basic authentication:

grafana = GrafanaFace(
          auth=("username","password"),
          host='api.my-grafana-host.com'
          )

# Use token
grafana = GrafanaFace(
          auth='abcdetoken...',
          host='api.my-grafana-host.com'
          )
```


## Status of REST API realization

Work on API implementation still in progress.

| API | Status |
|---|---|
| Admin | + |
| Alerting | - |
| Alerting Notification Channels | + |
| Annotations | + |
| Authentication | +- |
| Dashboard | + |
| Dashboard Versions | - |
| Dashboard Permissions | + |
| Data Source | + |
| Folder | + |
| Folder Permissions | + |
| Folder/Dashboard Search | +- |
| Organisation | + |
| Other | + |
| Preferences | + |
| Snapshot | + |
| Teams | + |
| User | + |


## Software tests

```shell
pip install pytest
pytest test
```

## Release

```shell
pip install pep517 twine
python -m pep517.build --source --binary --out-dir dist/ .
twine upload --repository=testpypi dist/*
```

## Issue tracker

Please report any bugs and enhancement ideas using the `grafana-client` issue tracker:

  https://github.com/panodata/grafana-client/issues

Feel free to also ask questions on the tracker.

## License

`grafana-client` is licensed under the terms of the MIT License (see the file
[LICENSE](LICENSE)).
