from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView, TemplateView

from .models import Question, Comment, Tag
from .forms import QuestionCreationForm, UserChangeInfoForm, AddCommentForm


class IndexView(ListView):
    template_name = 'questions/index.html'
    context_object_name = 'questions'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.prefetch_related('tags').order_by('-created_at')


class QuestionsByTagView(ListView):
    template_name = 'questions/by_tag.html'
    context_object_name = 'questions'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.prefetch_related('tags').filter(tags__name=self.kwargs['tag']).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag'] = self.kwargs['tag']
        return data


class QuestionsByUser(ListView):
    template_name = 'questions/by_user.html'
    context_object_name = 'questions'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.prefetch_related('tags').filter(author__username=self.kwargs['username']).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['username'] = self.kwargs['username']
        return data


class AllTagsView(ListView):
    template_name = 'questions/tags.html'
    model = Tag
    context_object_name = 'tags'
    paginate_by = 10

    def get_queryset(self):
        return Tag.objects.prefetch_related('questions_by_tag').all()


class SearchResultsView(ListView):
    template_name = 'questions/search_results.html'
    context_object_name = 'questions'
    paginate_by = 5

    def get_queryset(self):
        q = self.request.GET.get('q')
        return Question.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(author__username__icontains=q))


def detail_question(request, slug):
    question = get_object_or_404(Question.objects.select_related('author'), slug=slug)
    comments = question.comment_set.select_related('author').prefetch_related('likes').prefetch_related(
        'dislikes').all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('account_signup')
        form = AddCommentForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.author = request.user
            inst.question = question
            inst.save()

    form = AddCommentForm()
    context = {
        'question': question,
        'form': form,
        'comments': comments,
    }
    return render(request, 'questions/detail_question.html', context=context)


def question_creation(request):
    if request.method == 'POST':
        form = QuestionCreationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            tags = cd['tags'].split()
            tags = [tag.strip() for tag in tags]
            inst = form.save(commit=False)
            inst.author = request.user
            inst.save()
            print(tags)
            for tag in tags:
                now_tag, created = Tag.objects.get_or_create(name=tag)
                inst.tags.add(now_tag)
            return redirect('home')
    else:
        form = QuestionCreationForm()
    context = {
        'form': form
    }
    return render(request, 'questions/creation.html', context=context)


class ProfileView(TemplateView):
    template_name = 'account/profile.html'


def change_user_info(request):
    user = request.user
    if request.method == 'POST':
        form = UserChangeInfoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeInfoForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'questions/profile_change.html', context=context)


@login_required
@require_POST
def like_or_dislike_to_question(request, question_slug, is_like):
    user = request.user
    question = Question.objects.get(slug=question_slug)
    if is_like == 1:
        if question.dislikes.filter(username__in=[user.username]):
            question.dislikes.remove(user)
            question.likes.add(user)
        elif question.likes.filter(username__in=[user.username]):
            question.likes.remove(user)
        else:
            question.likes.add(user)
    else:
        if question.likes.filter(username__in=[user.username]):
            question.likes.remove(user)
            question.dislikes.add(user)
        elif question.dislikes.filter(username__in=[user.username]):
            question.dislikes.remove(user)
        else:
            question.dislikes.add(user)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def like_or_dislike_to_comment(request, comment_pk, is_like):
    user = request.user
    comment = Comment.objects.get(pk=comment_pk)
    if is_like == 1:
        if comment.dislikes.filter(username__in=[user.username]):
            comment.dislikes.remove(user)
            comment.likes.add(user)
        elif comment.likes.filter(username__in=[user.username]):
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
    else:
        if comment.likes.filter(username__in=[user.username]):
            comment.likes.remove(user)
            comment.dislikes.add(user)
        elif comment.dislikes.filter(username__in=[user.username]):
            comment.dislikes.remove(user)
        else:
            comment.dislikes.add(user)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def set_solution_to_comment(request, comment_pk, is_solution):
    comment = Comment.objects.get(pk=comment_pk)
    comment.is_solution = bool(is_solution)
    comment.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
