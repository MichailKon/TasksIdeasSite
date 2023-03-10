from django.urls import path

from .views import IdeaCreateView, IdeaDeleteView, IdeaUpdateView, IdeaListView, \
    delete_comment_by_user_request, update_comment_by_user_request, create_comment_by_user_request, idea_detail_view

urlpatterns = [
    path('', IdeaListView.as_view(), name='ideas-home'),
    path('idea/<int:pk>/', idea_detail_view, name='idea-detail'),
    path('idea/new/', IdeaCreateView.as_view(), name='idea-create'),
    path('idea/<int:pk>/update/', IdeaUpdateView.as_view(), name='idea-update'),
    path('idea/<int:pk>/delete/', IdeaDeleteView.as_view(), name='idea-delete'),
    path('idea/<int:pk>/new_comment', create_comment_by_user_request, name='comment-create'),
    path('comment/<int:pk>/delete/', delete_comment_by_user_request, name='comment-delete'),
    path('comment/<int:pk>/update', update_comment_by_user_request, name='comment-update')
]
