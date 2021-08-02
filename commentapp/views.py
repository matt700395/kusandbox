from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, DetailView, UpdateView

from commentapp.decorators import comment_ownership_required
from commentapp.forms import CommentCreationForm
from commentapp.models import Comment


@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentCreationForm
    template_name = 'commentapp/create.html'

    def form_valid(self, form):
        temp_comment = form.save(commit=False)
        temp_comment.writer = self.request.user
        temp_comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('commentapp:detail', kwargs={'pk': self.object.pk})

# class CommentDetailView(DetailView):
#     model = Comment
#     context_object_name = 'target_post'
#     template_name = 'commentapp/detail.html'
#
#     # def get_context_data(self, **kwargs):
#     #     post = self.object
#     #     user = self.request.user
#     #
#     #     #if user.is_authenticated: #로그인 했는가?
#     #        #join = Join.objects.filter(user=user, project=project)
#     #     #object_list = Post.object(project=self.get_object())
#     #     return super(PostDetailView, self).get_context_data(object_list=object_list, **kwargs)
#     #     #return super(PostDetailView, self).get_context_data(join=join, **kwargs)



@method_decorator(comment_ownership_required, 'get')
@method_decorator(comment_ownership_required, 'post')
class CommentUpdateView(UpdateView):
    model = Comment
    context_object_name = 'target_comment'
    form_class = CommentCreationForm
    template_name = 'commentapp/update.html'

    def get_success_url(self):
        return reverse('commentapp:detail', kwargs={'pk': self.object.pk})

@method_decorator(comment_ownership_required, 'get')
@method_decorator(comment_ownership_required, 'post')
class CommentDeleteView(DeleteView):
    model = Comment
    context_object_name = 'target_comment'
    success_url = reverse_lazy('commentapp:list')
    template_name = 'commentapp/delete.html'

class CommentListView(ListView):
    model = Comment
    context_object_name = 'comment_list'
    template_name = 'commentapp/list.html'
    paginate_by = 25

