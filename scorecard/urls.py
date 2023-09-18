from django.urls import path

from .views import (
    scorecard_create_view,
    scorecard_detail_view,
    scorecard_list_view,
    scorecard_update_view,
    scorecard_detail_hx_view,
    scorecard_children_update_hx_view,
    scorecard_delete_view,
    scorecard_children_delete_view,

)
app_name='scorecard'
urlpatterns = [
    path("",scorecard_list_view ,name = 'list'),
    path("create/",scorecard_create_view, name ='create'),
    path("<int:id>/edit/",scorecard_update_view, name='update'),
    path("<int:id>/",scorecard_detail_view,name = 'detail'),
    path("hx/<int:id>/",scorecard_detail_hx_view,name = 'hx-detail'),
    path("hx/<int:parent_id>/scorecard/<int:id>/",scorecard_children_update_hx_view,name = 'hx-scorecard-detail'),
    path("hx/<int:parent_id>/scorecard/",scorecard_children_update_hx_view,name = 'hx-scorecard-create'),
    path("<int:id>/delete/",scorecard_delete_view,name = 'delete'),
    path("<int:parent_id>/scorecard/<int:id>/delete/",scorecard_children_delete_view,name = 'scorecard-delete'),
]
