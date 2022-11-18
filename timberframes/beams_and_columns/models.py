from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .fields import BreadthDepthField

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
        max_length=20,
        choices=LUMBER_CHOICES,
        default="lumber",
        verbose_name="Lumber Type",
    )
    # grade = models.ForeignKey("Lumber_Grade", on_delete=models.CASCADE)
    # grade = models.ManyToManyField(Lumber_Grade)
    lumber_grade = models.CharField(
        max_length=20, choices=LUMBER_GRADE, default="no_2", verbose_name="Lumber Grade"
    )
    E = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="Modulus of Elasticity (psi)"
    )
    E_min = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name="Minimum Modulus of Elasticity (psi)",
    )
    G = models.DecimalField(
        max_digits=3, decimal_places=2, verbose_name="Specific Gravity"
    )
    F_v = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Design Shear Parallel to Grain (psi)",
    )
    F_c = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Design Compression Parallel to Grain (psi)",
    )
    F_c_perp = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Design Compression Perperdicular to Grain (psi)",
    )
    F_b = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Design Bending (psi)"
    )
    F_t = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Design Tension Parallel to Grain (psi)",
    )

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


class Lumber_Type_Grade_Size_Info(models.Model):
    """ "Things needed to make up a full lumber type

    Parameters
    ----------
    lumber_types : glulam, dimensional, uncut (?)
        Drop-down or Radial button
    lumber_grade : "select_structural","no_1","no_2", no_3","stud"
        Drop-down or Radial button
    lumber_size : Different tables for (2-4") and (5"x5" or larger)
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

    LUMBER_TYPES = (
        ("lumber", _("Cut Lumber")),
        ("glulam", _("Glulam")),
        ("log", _("Raw Log")),
    )
    LUMBER_GRADES = (
        ("select_structural", _("Select Structural")),
        ("no_1", _("No. 1")),
        ("no_2", _("No. 2")),
        ("no_3", _("No. 3")),
        ("stud", _("Stud")),
        # ("construction", _("Construction")),
        # ("standard", _("Standard")),
        # ("utility", _("Utility")),
    )
    LUMBER_SIZES = (
        ("regular", _("2-inch to 4-inch in width/breadth.")),
        ("large", _("Greater than 5-inches by 5-inches.")),
    )

    lumber_type = models.CharField(
        max_length=20,
        choices=LUMBER_TYPES,
        default="lumber",
        verbose_name="Lumber Type",
    )
    lumber_grade = models.CharField(
        max_length=20,
        choices=LUMBER_GRADES,
        default="no_2",
        verbose_name="Lumber Grade",
    )
    lumber_size = models.CharField(
        max_length=20,
        choices=LUMBER_SIZES,
        default="regular",
        verbose_name="Lumber Size",
    )
    E = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="Modulus of Elasticity (psi)"
    )
    E_min = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name="Minimum Modulus of Elasticity (psi)",
    )
    G = models.DecimalField(
        max_digits=3, decimal_places=2, verbose_name="Specific Gravity"
    )
    F_v = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Design Shear Parallel to Grain (psi)",
    )
    F_c = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Design Compression Parallel to Grain (psi)",
    )
    F_c_perp = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Design Compression Perperdicular to Grain (psi)",
    )
    F_b = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Design Bending (psi)"
    )
    F_t = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Design Tension Parallel to Grain (psi)",
    )

    def __str__(self):
        return str(self.lumber_type)


class Wood_Type_2(models.Model):
    """Things needed to make up a wood type

    Parameters
    ----------
    wood_name : str, Name of the wood
    lumber : Things needed to make up a full lumber type, grade, size, other info
    """

    wood_name = models.CharField(max_length=200)
    lumber = models.ManyToManyField(Lumber_Type_Grade_Size_Info)

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


class BreadthDepthModelField(models.Field):
    """Model Field to select inches and fractions of inches for breadth and depth models"""

    def formfield(self, **kwargs):
        defaults = {"form_class": BreadthDepthField}
        defaults.update(kwargs)
        return super(BreadthDepthModelField, self).formfield(**defaults)

    def db_type(self, connection):
        return "BreadthDepthField"


class Beams_and_Columns(models.Model):
    """
    Parameters
    ----------
    wood_type : object
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

    # wood_type = models.ManyToManyField(Wood_Type)
    wood_type = models.ForeignKey(
        "Wood_Type",
        on_delete=models.CASCADE,
        blank=True,
        default=1,
        verbose_name="Wood Type",
    )
    breadth = BreadthDepthModelField()
    depth = BreadthDepthModelField()

    class Meta:
        verbose_name = _("Beam and Column Calculation")
        verbose_name_plural = _("Beam and Column Calculations")

    def __str__(self):
        return _("Beam and Column Calculation")
