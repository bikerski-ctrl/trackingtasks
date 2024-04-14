from django.urls import path
from comments import views

urlpatterns = [
    path('<int:pk>/edit', views.CommentUpdateView.as_view(), name="comment_edit"),
    path('<int:pk>/delete', views.CommentDeleteView.as_view(), name="comment_delete"),
    path('<int:pk>/<str:action>/', views.CommentLikeDislikeView.as_view(), name="comment_action"),
]