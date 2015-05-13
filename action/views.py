from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from action.forms import ActionForm
from action import client


def new(request):
    form = ActionForm(request.POST or None)

    if form.is_valid():
        token = request.GET.get("TSURU_TOKEN")
        client.new(form.cleaned_data, token)
        messages.success(request, u"Action saved.")
        return redirect(reverse('action-list'))

    context = {"form": form}
    return render(request, "action/new.html", context)


def list(request):
    token = request.GET.get("TSURU_TOKEN")
    actions = client.list(token).json()
    context = {
        "list": actions,
    }
    return render(request, "action/list.html", context)


def get(request, name):
    token = request.GET.get("TSURU_TOKEN")
    action = client.get(name, token).json()
    context = {
        "item": action,
    }
    return render(request, "action/get.html", context)


def remove(request, name):
    token = request.GET.get("TSURU_TOKEN")
    client.remove(name, token)
    messages.success(request, u"Action {} removed.".format(name))
    return redirect(reverse('action-list'))
