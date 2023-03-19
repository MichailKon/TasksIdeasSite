from django.urls import path

from .views import get_idea, get_user_info, get_ideas_with_access, get_comment

urlpatterns = [path('idea/<int:idea_pk>', get_idea),
               path('user/<int:user_pk>', get_user_info),
               path('ideas', get_ideas_with_access),
               path('comment/<int:comment_pk>', get_comment)
               ]
