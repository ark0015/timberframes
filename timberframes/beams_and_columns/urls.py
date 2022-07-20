from django.urls import path

from .views import (
    BeamAndColumnFormView,
    WoodTypeDeleteView,
    WoodTypeDetailView,
    WoodTypeFormView,
    WoodTypeListView,
    WoodTypeUpdateView,
)

urlpatterns = [
    # path("", view=WoodTypeListView.as_view(), name="home"),
    path("", view=BeamAndColumnFormView.as_view(), name="home"),
    # path("wood_type", view=WoodTypeFormView.as_view(), name="wood_type"),
    # path("wood_type/", view=WoodTypeFormView.as_view(), name="wood_type"),
    path("wood_type/", view=WoodTypeListView.as_view(), name="wood_type_list"),
    path("wood_type/new", view=WoodTypeFormView.as_view(), name="wood_type_new"),
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
