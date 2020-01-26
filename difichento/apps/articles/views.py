from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from django.views.generic import TemplateView, FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .forms import MyForm  # Моя форма для регистрации
from .models import Article, Comment


def index(request):
    latest_articles_list = Article.objects.order_by('-pub_date')[:5]
    return render(request, 'articles/list.html', {'latest_articles_list': latest_articles_list})


def test(request):
    return HttpResponse('Отображение для тестовой ссылки')


class RegisterForm(FormView):
    form_class = MyForm

    success_url = 'articles/login/'

    template_name = 'articles/register.html'

    def form_valid(self, form):
        form.save()
        return super(RegisterForm, self).form_valid(form)


class LoginForm(FormView):

    # def __init__(self, user, **kwargs):  # Не понимаю. Без этих строк
    #     super().__init__(**kwargs)       # PyCharm ругается, но сайт не работает
    #     self.user = user                 # И наоборот, соответственно

    form_class = AuthenticationForm
    template_name = 'articles/login.html'
    success_url = '/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginForm, self).form_valid(form)


def detail(request, article_id):
    try:
        a = Article.objects.get(id=article_id)

    except Exception:
        raise Http404('Ошибка.')

    latest_comments_list = a.comment_set.order_by('-id')[:10]

    return render(request, 'articles/detail.html', {'article': a, 'latest_comments_list': latest_comments_list})


def leave_comment(request, article_id):
    try:
        a = Article.objects.get(id=article_id)

    except Exception:
        raise Http404('Ошибка!!1!!1!')

    a.comment_set.create(author_name=request.POST['name'], comment_text=request.POST['text'])

    return HttpResponseRedirect(reverse('articles:detail', args=(a.id,)))
