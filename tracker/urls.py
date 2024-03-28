from django.urls import path
from tracker import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name="task_list"),
    path('<int:pk>/', views.TaskDetailView.as_view(), name="task_detail"),
    path('add/', views.TaskCreate.as_view(), name="task_add"),
]
