from fractions import Fraction as frac

import numpy as np
from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

from .widgets import BreadthDepthWidget


class BreadthDepthField(forms.MultiValueField):
    """Field to select inches and fractions of inches for breadth and depth models"""

    def __init__(self, *args, **kwargs):
        # Define one message for all fields.

        # description = _("Field to select inches and fractions of inches for breadth and depth models.")
        kwargs["error_messages"] = {
            _("incomplete"): _("Enter an inch and a fraction of an inch.")
        }

        i_selections = []
        for x in np.arange(0, 16):
            if x == 1:
                i_selections.append((f"{x}", f"{x} inch"))
            else:
                i_selections.append((f"{x}", f"{x} inches"))
        INCH_SELECTIONS = tuple(i_selections)

        f_selections = []
        for x in np.arange(0, 16) / 16:
            f_selections.append((f"{x}", str(frac(x))))
        FRACTIONAL_SELECTIONS = tuple(f_selections)

        fields = (
            models.CharField(
                max_length=20,
                choices=INCH_SELECTIONS,
                default="0",
                verbose_name="Inches",
            ),
            models.CharField(
                max_length=20,
                choices=FRACTIONAL_SELECTIONS,
                default="0.0",
                verbose_name="Fraction of an Inch",
            ),
        )
        kwargs["widget"] = BreadthDepthWidget  # MultiWidget(widgets=[])
        super().__init__(
            fields,
            *args,
            **kwargs,
        )

    def compress(self, data_list):
        if data_list:
            return (",").join(data_list)
        return None
