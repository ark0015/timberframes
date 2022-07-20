from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Beams_and_Columns, Wood_Type


class BeamAndColumnForm(ModelForm):
    """
    Form for choosing the wood type, and dimensions.
    """

    class Meta:
        model = Beams_and_Columns
        fields = [
            "wood_type",
            # "lumber_type",
            # "lumber_grade",
            "breadth",
            "depth",
        ]
        labels = {
            "wood_type": _("Wood Type"),
            # "lumber_type": _("Lumber Type"),
            # "lumber_grade": _("Grade"),
            # "size": _("Size"),
            "breadth": _("Breadth of the Wood"),
            "depth": _("Depth of the Wood"),
        }


class WoodTypeForm(ModelForm):
    """
    Form for creating type of wood and its properties
    """

    class Meta:
        model = Wood_Type
        fields = [
            "wood_name",
            "lumber_type",
            "lumber_grade",
            # "size",
            "E",
            "E_min",
            "G",
            "F_v",
            "F_c",
            "F_c_perp",
            "F_b",
            "F_t",
        ]
        labels = {
            "wood_name": _("Wood Name"),
            "lumber_type": _("Lumber Type"),
            "lumber_grade": _("Grade"),
            # "size": _("Size"),
            "E": _("Modulus of Elasticity"),
            "E_min": _("Minimum Modulus of Elasticity"),
            "G": _("Specific Gravity"),
            "F_v": _("Shear Parallel to Grain"),
            "F_c": _("Compression Parallel to Grain"),
            "F_c_perp": _("Compression Perperdicular to Grain"),
            "F_b": _("Bending"),
            "F_t": _("Tension Parallel to Grain"),
        }
