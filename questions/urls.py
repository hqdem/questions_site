from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('tags/', AllTagsView.as_view(), name='show_all_tags'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('questions/<str:username>/', QuestionsByUser.as_view(), name='questions_by_user'),
    path('tagged/<str:tag>/', QuestionsByTagView.as_view(), name='questions_by_tag'),
    path('question/<slug:slug>/', detail_question, name='question_detail'),
    path('create_question/', question_creation, name='question_creation'),
    path('accounts/profile/', login_required(ProfileView.as_view()), name='profile'),
    path('change_user_info/', change_user_info, name='change_user_info'),
    path('questions_like_or_dislike/<slug:question_slug>/<int:is_like>/', like_or_dislike_to_question, name='like_or_dislike_to_question'),
    path('comment_like_or_dislike/<str:comment_pk>/<int:is_like>/', like_or_dislike_to_comment, name='like_or_dislike_to_comment'),
    path('set_solution_to_comment/<str:comment_pk>/<int:is_solution>/', set_solution_to_comment, name='set_solution_to_comment'),
]
