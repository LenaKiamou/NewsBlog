from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_article", views.create, name="create"),
    path("all_news", views.news_view, name="all_news"),
    path("article/<str:title>", views.article_view, name="article"),
    path("profile/<str:username>", views.profile_view, name="profile"),
    path("search", views.search, name="search"),
    path("edit/<str:id>", views.edit, name="edit"),
    path("categories/<str:category_id>", views.category_view, name='category'),
    path("authors", views.authors_view, name="authors"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("favorites", views.favorites, name="favorites"),
    path("unpublished", views.unpublished, name="unpublished"),
    path("publish/<str:id>", views.publish, name="publish"),
    path("delete/<str:id>", views.delete, name="delete"),
]
