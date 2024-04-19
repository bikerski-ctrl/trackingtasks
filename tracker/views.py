from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Exists, OuterRef, Count
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from tracker.models import Task
from tracker.forms import TaskForm, TaskFilterForm
from tracker.mixins import UserIsOwnerMixin
from comments.models import Comment
from comments.forms import CommentForm

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tracker/task_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if status := self.request.GET.get("status", ""):
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)
        return context


class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tracker/task_detail.html'

    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(Task, pk=task_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(task=self.get_object())
        comments = comments.annotate(
            liked=Exists(Comment.likes.through.objects.filter(comment_id=OuterRef('pk'), user_id=self.request.user.id)),
            disliked=Exists(Comment.dislikes.through.objects.filter(comment_id=OuterRef('pk'), user_id=self.request.user.id)),
            num_likes=Count('likes'),
            num_dislikes=Count('dislikes')
        )
        context['comments'] = comments
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        form = CommentForm(request.POST, request.FILES)
        form.instance.author = self.request.user
        form.instance.task = self.get_object()
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(self.request.path_info)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tracker/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def post(self, _request, *args, **kwargs):
        task = self.get_object()
        task.status = "done"
        task.save()
        return HttpResponseRedirect(reverse_lazy("task_list"))


    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(Task, pk=task_id)


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tracker/task_update_form.html"
    success_url = reverse_lazy("task_list")


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = "tracker/task_delete_confirmation.html"
    success_url = reverse_lazy("task_list")
