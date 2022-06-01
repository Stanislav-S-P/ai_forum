from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView

from app_forum.forms import MyForm, NewsFullForm, CommentsForm
from app_forum.models import News, Images


class AnotherLoginView(LoginView):
    """
    Класс-контроллер для авторизации пользователя
    """
    template_name = 'users/login.html'
    next_page = '/'


class AnotherLogoutView(LogoutView):
    """
    Класс-контроллер для выхода из аккаунта пользователя
    """
    template_name = 'users/logout.html'


class SignUpView(CreateView):
    """
    Класс-контроллер регистрации аккаунта пользователя
    """
    form_class = MyForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class NewsListView(ListView):
    """
    Класс-контроллер главной страницы (списка новостей)
    """
    model = News
    template_name = 'forum/home.html'
    context_object_name = 'news'
    queryset = News.objects.all()

    def get_ordering(self):
        """
        Функция переопределяющая метод get_ordering.
        Предназначена для сортировки новостей по дате создания новости.
        """
        ordering = self.request.GET.get('orderby')
        if ordering == 'По возрастанию':
            ordering = 'created_at'
        else:
            ordering = '-created_at'
        return ordering


class NewsDetailView(DetailView):
    """
    Класс-контроллер детальной страницы новостей.
    """
    model = News
    template_name = 'forum/news_detail.html'
    context_object_name = 'news'
    queryset = News.objects.all()

    def get_context_data(self, **kwargs):
        """
        Функция переопределяющая метод get_context_data.
        Добавляет в контекст к новости Изображение, Форму для комментариев и Комментарии
        """
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.all()
        comments_form = CommentsForm()
        images = self.object.images.all()
        context['comments'] = comments
        context['comments_form'] = comments_form
        context['images'] = images
        return context

    def post(self, request, *args, **kwargs):
        """
        Функция-контроллер переопределяющая метод post. Сохраняет комментарии.
        """
        comments_form = CommentsForm(request.POST)
        if comments_form.is_valid():
            comment = comments_form.save(commit=False)
            comment.new = self.get_object()
            if request.user.is_authenticated:
                comment.user = request.user
                comment.user_name = request.user.username
            else:
                comment.user_name += '  "anonymous"'
            comment.save()
            return HttpResponseRedirect(reverse('news_detail', kwargs={'pk': comment.new.id}))
        context = self.get_context_data()
        context.update({'comments_form': comments_form})
        return render(request, 'forum/news_detail.html', context=context)


def add_news_view(request):
    """
    Функция-контроллер, при GET запросе выводит форму для добавления новости,
    при POST запросе сохраняет новость.
    """
    if request.method == 'POST':
        form = NewsFullForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('images')
        if form.is_valid():
            author = request.user
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            new = News.objects.create(author=author, title=title, description=description)
            for f in files:
                Images.objects.create(news=new, image=f)
            return redirect('home')
    else:
        form = NewsFullForm()
    return render(request, 'forum/create_news.html', {'form': form})
