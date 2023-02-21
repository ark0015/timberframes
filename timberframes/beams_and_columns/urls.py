from django.urls import path

from .views import (
    BeamAndColumnFormView,
    BeamAndColumnResultsView,
    WoodTypeDeleteView,
    WoodTypeDetailView,
    WoodTypeFormView,
    WoodTypeListView,
    WoodTypeUpdateView,
)

urlpatterns = [
    # path("", view=WoodTypeListView.as_view(), name="home"),
    path("", view=BeamAndColumnFormView.as_view(), name="home"),
    path(
        "results/<int:pk>/",
        view=BeamAndColumnResultsView.as_view(),
        name="beams_and_columns_results",
    ),
    path(
        "results/<int:pk>/",
        view=BeamAndColumnResultsView.as_view(),
        name="beams_and_columns_results",
    ),
    # path("wood_type", view=WoodTypeFormView.as_view(), name="wood_type"),
    # path("wood_type/", view=WoodTypeFormView.as_view(), name="wood_type"),
    path("wood_type/", view=WoodTypeListView.as_view(), name="wood_type_list"),
    path("wood_type/new", view=WoodTypeFormView.as_view(), name="wood_type_form"),
    path(
        "wood_type/<int:pk>/",
        WoodTypeDetailView.as_view(),
        name="wood_type_detail",
    ),
    path(
        "wood_type/<int:pk>/edit",
        WoodTypeUpdateView.as_view(),
        name="wood_type_edit",
    ),
    path(
        "wood_type/<int:pk>/delete",
        view=WoodTypeDeleteView.as_view(),
        name="wood_type_delete",
    ),
]
