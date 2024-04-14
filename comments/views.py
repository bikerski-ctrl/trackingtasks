from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, UpdateView, DeleteView
from comments.mixins import UserIsOwnerMixin
from comments.models import Comment
from comments.forms import CommentForm

class CommentLikeDislikeView(LoginRequiredMixin, View):
    def post(self, request, pk, action):
        comment = get_object_or_404(Comment, pk=pk)
        comment.likes.prefetch_related('user').all()
        comment.dislikes.prefetch_related('user').all()

        if action == 'like':
            if request.user not in comment.likes.all():
                comment.likes.add(request.user)
                if request.user in comment.dislikes.all():
                    comment.dislikes.remove(request.user)
            else:
                comment.likes.remove(request.user)
        elif action == 'dislike':
            if request.user not in comment.dislikes.all():
                comment.dislikes.add(request.user)
                if request.user in comment.likes.all():
                    comment.likes.remove(request.user)
            else:
                comment.dislikes.remove(request.user)

        comment.save()
        task_url = reverse_lazy("task_detail", kwargs={'pk':comment.task.pk})
        return redirect(f'{task_url}#{comment.pk}')


class CommentUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_update.html'
    
    def get_success_url(self, **kwargs):
        task_url = reverse_lazy("task_detail", kwargs={"pk":self.get_object().task.pk})
        pk = self.get_object().pk
        return f'{task_url}#{pk}'


class CommentDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Comment
    template_name = 'comments/comment_delete_confirm.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy("task_detail", kwargs={"pk":self.get_object().task.pk})