from django.urls import path

from .views import IdeaCreateView, idea_delete_view, IdeaUpdateView, IdeaListView, idea_detail_view

urlpatterns = [
    path('', IdeaListView.as_view(), name='ideas-home'),
    path('idea/<int:pk>/', idea_detail_view, name='idea-detail'),
    path('idea/new/', IdeaCreateView.as_view(), name='idea-create'),
    path('idea/<int:pk>/update/', IdeaUpdateView.as_view(), name='idea-update'),
    path('idea/<int:pk>/delete/', idea_delete_view, name='idea-delete')
]
