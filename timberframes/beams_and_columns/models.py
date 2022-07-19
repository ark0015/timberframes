from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# from django.contrib import admin

# Create your models here.


class Wood_Type(models.Model):
    """Things needed to make up a wood type

    Parameters
    ----------
    lumber_types : glulam, dimensional, uncut (?)
        Drop-down or Radial button
    grade
        Drop-down or Radial button
    size : Different tables for (2-4") and (5"x5" or larger)
        Drop-down or Radial button
    E : modulus of elasticity (psi)
        * Short Float
        * Include units with drop-down
    E_min : minimum modulus of elasticity (psi)
        * Short Float
        * Include units with drop-down
    G : specific gravity
        * Short Float
        * Include units with drop-down
    F_v : design shear parallel to grain (psi)
        * Short Float
        * Include units with drop-down
    F_c : design compression parallel to grain (psi)
        * Short Float
        * Include units with drop-down
    F_c_perp : design compression perperdicular to grain (psi)
        * Short Float
        * Include units with drop-down
    F_b : design bending (psi)
        * Short Float
        * Include units with drop-down
    F_t : design tension parallel to grain (psi)
        * Short Float
        * Include units with drop-down
    """

    LUMBER_CHOICES = (
        ("lumber", _("Cut Lumber")),
        ("glulam", _("Glulam")),
        ("log", _("Raw Log")),
    )
    LUMBER_GRADE = (
        ("select_structural", _("Select Structural")),
        ("no_1", _("No. 1")),
        ("no_2", _("No. 2")),
        ("no_3", _("No. 3")),
        ("stud", _("Stud")),
        # ("construction", _("Construction")),
        # ("standard", _("Standard")),
        # ("utility", _("Utility")),
    )

    wood_name = models.CharField(max_length=200)
    # lumber_type = models.ForeignKey("Lumber_Type", on_delete=models.CASCADE)
    # lumber_type = models.ManyToManyField(Lumber_Type)
    lumber_type = models.CharField(
        max_length=20, choices=LUMBER_CHOICES, default="lumber"
    )
    # grade = models.ForeignKey("Lumber_Grade", on_delete=models.CASCADE)
    # grade = models.ManyToManyField(Lumber_Grade)
    lumber_grade = models.CharField(max_length=20, choices=LUMBER_GRADE, default="no_2")
    E = models.DecimalField(max_digits=7, decimal_places=2)
    E_min = models.DecimalField(max_digits=7, decimal_places=2)
    G = models.DecimalField(max_digits=7, decimal_places=2)
    F_v = models.DecimalField(max_digits=7, decimal_places=2)
    F_c = models.DecimalField(max_digits=7, decimal_places=2)
    F_c_perp = models.DecimalField(max_digits=7, decimal_places=2)
    F_b = models.DecimalField(max_digits=7, decimal_places=2)
    F_t = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = "Wood Type"
        verbose_name_plural = "Wood Types"

    def __str__(self):
        return str(self.wood_name)

    def get_absolute_url(self):
        return reverse("wood_type_detail", args=[str(self.id)])

    def get_fields(self):
        return [
            (field.name, field.value_to_string(self)) for field in self._meta.fields
        ]


# class Lumber(models.Model):
#    """Used to select different,
#        lumber types: glulam, dimensional, uncut (?),
#        lumber size: Different tables for (2-4") and (5"x5" or larger) and
#        Grades"""
#    lumber_type = "Nothing Yet."
#    lumber_grade = "Nothing Yet."
#    lumber_size = "Nothing Yet."
#    def __str__(self):
#        return self.lumber_type


class Lumber_Type(models.Model):
    """Used to select different lumber types: glulam, dimensional, uncut (?)"""

    lumber_type = "Nothing Yet."
    pass

    def __str__(self):
        return str(self.lumber_type)


class Lumber_Grade(models.Model):
    """Used to select different Grades"""

    lumber_grade = "Nothing Yet."
    pass

    def __str__(self):
        return str(self.lumber_grade)


class Lumber_Size(models.Model):
    """Used to select different lumber size: Different tables for (2-4") and (5"x5" or larger)"""

    lumber_size = "Nothing Yet."
    pass

    def __str__(self):
        return str(self.lumber_size)


class Beams_and_Columns(models.Model):
    """
    Parameters
    ----------
    wood_choice : object
        type of wood (oak, pine, etc.)
    lumber_types : glulam, dimensional, uncut (?)
        * Drop-down or Radial button
    grade
        * Drop-down or Radial button
    size : Different tables for (2-4") and (5"x5" or larger)
        - breadth
            * Short Float
            * Include units with drop-down
        - depth
            * Short Float
            * Include units with drop-down
    """

    # wood_choice = models.ManyToManyField(Wood_Type)
    wood_choice = models.ForeignKey(
        "Wood_Type", on_delete=models.CASCADE, blank=True, default=1
    )
    breadth = models.DecimalField(max_digits=5, decimal_places=2)
    depth = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = _("Beam and Column Calculation")
        verbose_name_plural = _("Beam and Column Calculations")

    def __str__(self):
        return _("Beam and Column Calculation")
