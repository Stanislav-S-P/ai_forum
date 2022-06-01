from django.urls import path
from app_forum.views import AnotherLoginView, AnotherLogoutView, SignUpView, NewsListView, add_news_view, NewsDetailView

urlpatterns = [
    path('login/', AnotherLoginView.as_view(), name='login'),
    path('logout/', AnotherLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', NewsListView.as_view(), name='home'),
    path('add_news/', add_news_view, name='add_news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
]
