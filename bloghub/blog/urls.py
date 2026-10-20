from django.urls import path
from . import views

urlpatterns = [
    path("",views.PostListView.as_view(),name="post_list"),
    path("fbv", views.post_list_fbv, name="post_fbv_list"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("ping/", views.PingView.as_view(), name="ping"),
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("post/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("stats/", views.stats, name="stats"),
]