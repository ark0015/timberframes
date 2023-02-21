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
            "user_selected_support_type",
            "breadth",
            "depth",
            "length",
        ]
        labels = {
            "wood_type": _("What type of wood are you using?"),
            # "lumber_type": _("Lumber Type"),
            # "lumber_grade": _("Grade"),
            # "size": _("Size"),
            "user_selected_support_type": _(
                "What type of support are you looking to stress test?"
            ),
            "breadth": _("What is the breadth of your support?"),
            "depth": _("What is the depth of your support?"),
            "length": _(
                "What is the unsupported span of your system (vertical or horizontal)?"
            ),
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
