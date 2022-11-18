# import re
from fractions import Fraction as frac

import numpy as np
from django import forms


class BreadthDepthWidget(forms.MultiWidget):
    def __init__(self, attrs=None):

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

        widgets = (
            forms.Select(attrs=attrs, choices=INCH_SELECTIONS),
            forms.Select(attrs=attrs, choices=FRACTIONAL_SELECTIONS),
        )
        super(BreadthDepthWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            splt_value = value.split(",")
            return [splt_value[0], splt_value[1]]
        else:
            return [None, None]


"""
def value_from_datadict(self, data, files, name):
    day, month, year = super().value_from_datadict(data, files, name)
    # DateField expects a single string that it can parse into a date.
    return '{}-{}-{}'.format(year, month, day)
"""
