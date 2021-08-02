from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, DetailView, UpdateView

from boardapp.decorators import board_ownership_required
from boardapp.forms import BoardCreationForm
from boardapp.models import Board


@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class BoardCreateView(CreateView):
    model = Board
    form_class = BoardCreationForm
    template_name = 'boardapp/create.html'

    def form_valid(self, form):
        temp_board = form.save(commit=False)
        temp_board.writer = self.request.user
        temp_board.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('boardapp:detail', kwargs={'pk': self.object.pk})

class BoardDetailView(DetailView):
    model = Board
    context_object_name = 'target_post'
    template_name = 'boardapp/detail.html'



    # def get_context_data(self, **kwargs):
    #     post = self.object
    #     user = self.request.user
    #
    #     #if user.is_authenticated: #로그인 했는가?
    #        #join = Join.objects.filter(user=user, project=project)
    #     #object_list = Post.object(project=self.get_object())
    #     return super(PostDetailView, self).get_context_data(object_list=object_list, **kwargs)
    #     #return super(PostDetailView, self).get_context_data(join=join, **kwargs)



@method_decorator(board_ownership_required, 'get')
@method_decorator(board_ownership_required, 'post')
class BoardUpdateView(UpdateView):
    model = Board
    context_object_name = 'target_post'
    form_class = BoardCreationForm
    template_name = 'boardapp/update.html'

    def get_success_url(self):
        return reverse('boardapp:detail', kwargs={'pk': self.object.pk})

@method_decorator(board_ownership_required, 'get')
@method_decorator(board_ownership_required, 'post')
class BoardDeleteView(DeleteView):
    model = Board
    context_object_name = 'target_post'
    success_url = reverse_lazy('boardapp:list')
    template_name = 'boardapp/delete.html'



class BasicListView(ListView):
    model = Board
    context_object_name = 'post_list'

    #template_name = 'boardapp/notice.html'
    paginate_by = 25

    ordering = ['-id']



class BoardListView(BasicListView):
    template_name = 'boardapp/list.html'



class NoticeListView(BasicListView):
    template_name = 'boardapp/notice.html'

    def get_queryset(self):
        temp = []
        board_all = Board.objects.all()
        for board in board_all:
            if board.type == 'notice':
                temp.append(board)
        board_temp = temp
        page = int(self.request.GET.get('p', 1))
        paginator = Paginator(board_temp, 3)
        queryset = paginator.get_page(page)
        return queryset

class ContestListView(BasicListView):
    template_name = 'boardapp/contest.html'


class KquestionListView(BasicListView):
    template_name = 'boardapp/kquestion.html'


class TutoringListView(BasicListView):
    template_name = 'boardapp/tutoring.html'


class DsumListView(BasicListView):
    template_name = 'boardapp/dsum.html'
