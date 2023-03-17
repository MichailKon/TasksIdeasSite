from django.urls import path

from .views import create_comment_by_user_request, delete_comment_by_user_request, update_comment_by_user_request

urlpatterns = [path('idea/<int:pk>/new_comment', create_comment_by_user_request, name='comment-create'),
               path('idea/<int:pk>/new_comment/<int:in_reply>', create_comment_by_user_request, name='comment-reply'),
               path('comment/<int:pk>/delete/', delete_comment_by_user_request, name='comment-delete'),
               path('comment/<int:pk>/update', update_comment_by_user_request, name='comment-update')
               ]
