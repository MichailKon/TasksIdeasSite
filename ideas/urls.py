from django.urls import path
from .views import IdeaCreateView, IdeaDeleteView, IdeaDetailView, IdeaUpdateView
from .views import render_home

from .models import Idea

urlpatterns = [
    path('', render_home, name='ideas-home'),
    # path('', IdeaListView.as_view(), name='ideas-home'),
    path('idea/<int:pk>/', IdeaDetailView.as_view(), name='idea-detail'),
    path('idea/new/', IdeaCreateView.as_view(), name='idea-create'),
    path('idea/<int:pk>/update/', IdeaUpdateView.as_view(), name='idea-update'),
    path('idea/<int:pk>/delete/', IdeaDeleteView.as_view(), name='idea-delete')
]
