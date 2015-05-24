from django.test import TestCase
from django.core.urlresolvers import reverse

from wizard import forms


class ScaleFormTest(TestCase):
    def test_required_fields(self):
        fields = {
            "metric": True,
            "operator": True,
            "value": True,
            "units": True,
            "wait": True,
        }

        form = forms.ScaleForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)


class ConfigFormTest(TestCase):
    def test_required_fields(self):
        fields = {
            "min": True,
        }

        form = forms.ConfigForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)


class IndexTestCase(TestCase):
    def test_index(self):
        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-index"))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "wizard/index.html")

    def test_forms_prefix(self):
        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-index"))
        response = self.client.get(url)

        forms = {
            "scale_up_form": "scale_up",
            "scale_down_form": "scale_down",
        }

        for f, prefix in forms.items():
            self.assertEqual(response.context[f].prefix, prefix)
