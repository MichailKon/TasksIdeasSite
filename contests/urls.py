from django.urls import path

from .views import ContestListView, contest_detail_view, ContestUpdateView, ContestCreateView, contest_delete_view

urlpatterns = [
    path('contests/', ContestListView.as_view(), name='contests-home'),
    path('contests/<int:pk>', contest_detail_view, name='contest-detail'),
    path('contests/<int:pk>/update/', ContestUpdateView.as_view(), name='contest-update'),
    path('contests/new', ContestCreateView.as_view(), name='contest-create'),
    path('contests/<int:pk>/delete', contest_delete_view, name='contest-delete')
]
