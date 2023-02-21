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
        self.assertEqual(
            self.wood_type.get_absolute_url(), f"/wood_type/{self.wood_type.id}/"
        )

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
        response = self.client.get(reverse("wood_type_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Spruce-Pine-Fir")
        self.assertTemplateUsed(response, "beams_and_columns/wood_type_list.html")

    def test_wood_type_detail_view(self):
        response = self.client.get(f"/wood_type/{self.wood_type.id}/")
        no_response = self.client.get("/wood_type/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Spruce-Pine-Fir")
        self.assertTemplateUsed(response, "beams_and_columns/wood_type_detail.html")

    def test_wood_type_create_view(self):
        response = self.client.post(
            reverse("wood_type_form"),
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
        response = self.client.post(
            reverse("wood_type_edit", args=f"{self.wood_type.id}"),
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


# For some reason pytest is doing things in alphabetical order which causes
# the wood_type to be deleted before other tests use it.
class WoodTypeDeleteTests(TestCase):
    def setUp(self):
        self.wood_type_2 = Wood_Type.objects.create(
            wood_name="Spruce-Pine-Fir",
            lumber_type="lumber",
            lumber_grade="select_structural",
            E=1.5e6,
            E_min=5.5e5,
            G=0.42,
            F_v=135,
            F_c=1400,
            F_c_perp=425,
            F_b=1250,
            F_t=700,
        )

    def test_wood_type_delete_view(self):
        response = self.client.post(
            reverse("wood_type_delete", args=f"{self.wood_type_2.id}")
        )
        self.assertEqual(response.status_code, 302)
