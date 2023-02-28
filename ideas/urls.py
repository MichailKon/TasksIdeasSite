from django.urls import path

from .views import IdeaCreateView, IdeaDeleteView, IdeaUpdateView, IdeaListView, idea_detail_view, \
    profile_ideas_list_view

urlpatterns = [
    path('', IdeaListView.as_view(), name='ideas-home'),
    path('idea/<int:pk>/', idea_detail_view, name='idea-detail'),
    path('idea/new/', IdeaCreateView.as_view(), name='idea-create'),
    path('idea/<int:pk>/update/', IdeaUpdateView.as_view(), name='idea-update'),
    path('idea/<int:pk>/delete/', IdeaDeleteView.as_view(), name='idea-delete'),
    path('profile/<int:pk>/', profile_ideas_list_view, name='profile-idea-list-view')
]
