from django.test import TestCase

from action.forms import ActionForm
from action import client

import httpretty
import mock

import os


class RemoveTestCase(TestCase):
    @mock.patch("action.client.list")
    @mock.patch("action.client.remove")
    def test_new_post(self, remove_mock, list_mock):
        response = self.client.delete("/action/name/")

        self.assertRedirects(response, '/action/')
        remove_mock.assert_called_with("name")


class NewTestCase(TestCase):
    def test_new(self):
        response = self.client.get("/action/new/")
        self.assertTemplateUsed(response, "action/new.html")
        self.assertIsInstance(response.context['form'], ActionForm)
        self.assertFalse(response.context['form'].is_bound)

    def test_new_invalid_post(self):
        response = self.client.post("/action/new/", {})
        self.assertFalse(response.context['form'].is_valid())

    @mock.patch("action.client.list")
    @mock.patch("action.client.new")
    def test_new_post(self, new_mock, list_mock):
        data = {
            'url': u'someurl',
            'body': u'',
            'headers': u'',
            'name': u'name',
            'method': u'GET',
        }

        response = self.client.post("/action/new/", data)

        self.assertRedirects(response, '/action/')
        new_mock.assert_called_with(data)


class ListTestCase(TestCase):
    @mock.patch("action.client.list")
    def test_list(self, list_mock):
        response = self.client.get("/action/")

        self.assertTemplateUsed(response, "action/list.html")
        self.assertIn('list', response.context)
        list_mock.assert_called_with()


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
            "http://autoscalehost.com/action",
        )

        client.list()

    def test_new(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.POST,
            "http://autoscalehost.com/action",
        )

        client.new({})

    def test_remove(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.DELETE,
            "http://autoscalehost.com/action/name",
        )

        client.remove("name")


class ActionFormTestCase(TestCase):
    def test_required_fields(self):
        fields = {
            "url": True,
            "method": True,
            "name": True,
            "body": False,
            "headers": False,
        }

        form = ActionForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)
