from django.urls import path
from tracker import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name="task_list"),
    path('<int:pk>/', views.TaskDetailView.as_view(), name="task_detail"),
    path('<int:pk>/update', views.TaskUpdateView.as_view(), name="task_update"),
    path('<int:pk>/complete', views.TaskCompleteView.as_view(), name="task_complete"),
    path('<int:pk>/delete', views.TaskDeleteView.as_view(), name="task_delete"),
    path('add/', views.TaskCreate.as_view(), name="task_add"),
]
