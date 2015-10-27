from django.shortcuts import render

from instance import client
from wizard import client as wclient

import urllib


def index(request, app):
    token = request.GET.get("TSURU_TOKEN")
    instances = client.list(token).json() or []

    instance = None
    auto_scale = None
    events = None

    for inst in instances:
        if app in inst.get('Apps', []):
            instance = inst

            response = wclient.get(instance["Name"], token)
            if response.status_code == 200:
                auto_scale = response.json()
                events = wclient.events(instance["Name"], token).json()
    context = {
        "instance": instance,
        "auto_scale": auto_scale,
        "token": urllib.quote(token),
        "app": app,
        "events": events,
    }
    return render(request, "app/index.html", context)
