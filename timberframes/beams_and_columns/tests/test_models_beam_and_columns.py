import pytest
from django.test import TestCase
from django.urls import reverse

from timberframes.beams_and_columns.models import Wood_Type

pytestmark = pytest.mark.django_db


class WoodTypeTests(TestCase):
    def setUp(self):
        self.wood_type = Wood_Type.objects.create(
            wood_name="Spruce-Pine-Fir",
            lumber_type="lumber",
            lumber_grade="no_2",
            E=1.4e6,
            E_min=5.1e5,
            G=0.42,
            F_v=135,
            F_c=1150,
            F_c_perp=425,
            F_b=875,
            F_t=450,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.wood_type), self.wood_type.wood_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.wood_type.get_absolute_url(), "/wood_type/1/")

    def test_wood_type_content(self):
        self.assertEqual(self.wood_type.wood_name, "Spruce-Pine-Fir")
        self.assertEqual(self.wood_type.lumber_type, "lumber")
        self.assertEqual(self.wood_type.lumber_grade, "no_2")
        self.assertEqual(self.wood_type.E, 1.4e6)
        self.assertEqual(self.wood_type.E_min, 5.1e5)
        self.assertEqual(self.wood_type.G, 0.42)
        self.assertEqual(self.wood_type.F_v, 135)
        self.assertEqual(self.wood_type.F_c, 1150)
        self.assertEqual(self.wood_type.F_c_perp, 425)
        self.assertEqual(self.wood_type.F_b, 875)
        self.assertEqual(self.wood_type.F_t, 450)

    def test_wood_type_list_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Spruce-Pine-Fir")
        self.assertTemplateUsed(response, "home.html")

    def test_wood_type_detail_view(self):
        response = self.client.get("/wood_type/1/")
        no_response = self.client.get("/wood_type/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Spruce-Pine-Fir")
        self.assertTemplateUsed(response, "wood_type_detail.html")

    def test_wood_type_create_view(self):
        response = self.client.wood_type(
            reverse("wood_type_new"),
            {
                "wood_name": "Red Oak",
                "lumber_type": "log",
                "lumber_grade": "no_1",
                "E": 1.2e6,
                "E_min": 4.4e5,
                "G": 0.67,
                "F_v": 155,
                "F_c": 775,
                "F_c_perp": 820,
                "F_b": 1000,
                "F_t": 675,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Wood_Type.objects.last().wood_name, "Red Oak")
        self.assertEqual(Wood_Type.objects.last().lumber_type, "log")

    def test_wood_type_update_view(self):
        response = self.client.wood_type(
            reverse("wood_type_edit", args="1"),
            {
                "lumber_type": "log",
                "lumber_grade": "no_2",
                "E": 1e6,
                "E_min": 3.7e5,
                "G": 0.67,
                "F_v": 155,
                "F_c": 350,
                "F_c_perp": 820,
                "F_b": 575,
                "F_t": 400,
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_wood_type_delete_view(self):
        response = self.client.wood_type(reverse("wood_type_delete", args="1"))
        self.assertEqual(response.status_code, 302)
