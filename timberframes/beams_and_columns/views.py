from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import BeamAndColumnForm, WoodTypeForm
from .models import Beams_and_Columns, Wood_Type

"""Wood Type Form"""


class WoodTypeListView(ListView):
    model = Wood_Type
    template_name = "beams_and_columns/wood_type_list.html"


class WoodTypeDetailView(DetailView):
    model = Wood_Type
    template_name = "beams_and_columns/wood_type_detail.html"
    # success_url = reverse_lazy("wood_type_detail")


class WoodTypeFormView(CreateView):
    model = Wood_Type
    form_class = WoodTypeForm
    template_name = "beams_and_columns/wood_type_form.html"
    # template_name = "beams_and_columns/b_n_c_detail.html"
    slug_field = "wood_type"
    slug_url_kwarg = "wood_type"
    context_object_name = "wood_type"


class WoodTypeUpdateView(UpdateView):
    model = Wood_Type
    template_name = "beams_and_columns/wood_type_edit.html"
    fields = [
        # "wood_name",
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


class WoodTypeDeleteView(DeleteView):
    model = Wood_Type
    form_class = WoodTypeForm
    template_name = "beams_and_columns/wood_type_delete.html"
    success_url = reverse_lazy("wood_type_list")


"""Beam and Column Form"""


class BeamAndColumnFormView(CreateView):
    model = Beams_and_Columns
    form_class = BeamAndColumnForm
    template_name = "pages/home.html"
    # success_url = reverse_lazy('beams_and_columns_results')
    # slug_field = "beams_and_columns"
    # slug_url_kwarg = "beams_and_columns"
    # context_object_name = "beams_and_columns"


class BeamAndColumnResultsView(DetailView):
    model = Beams_and_Columns
    template_name = "beams_and_columns/beams_and_columns_results.html"
    # success_url = reverse_lazy("beams_and_columns_results")
