import os

import requests


def host():
    return os.environ.get("AUTOSCALE_HOST", "")


def list(token):
    url = "{}/service/instance".format(host())
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response