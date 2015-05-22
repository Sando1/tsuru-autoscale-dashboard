from django.test import TestCase
from django.core.urlresolvers import reverse

from instance import client

import httpretty
import mock

import os


class ListTestCase(TestCase):
    @mock.patch("instance.client.list")
    def test_list(self, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("instance-list"))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "instance/list.html")
        self.assertIn('list', response.context)
        list_mock.assert_called_with("bla")


class ClientTestCase(TestCase):
    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_list(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/service/instance",
        )

        client.list("token")

    def test_get(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/service/instance/name",
        )

        client.get("name", "token")
