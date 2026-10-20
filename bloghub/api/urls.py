from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from . import views

router = DefaultRouter()
router.register("posts", views.PostViewSet,basename="post")  # basename needed: we override get_queryset

urlpatterns = [
    path("",include(router.urls)),
    path("register/", views.RegisterView.as_view()),
    path("me/", views.MeView.as_view()),
    path("categories/", views.CategoryListCreate.as_view()),

    path("categories-fbv/", views.category_list),
    path("tags/", views.TagListView.as_view()),
    path("tags/<int:pk>/", views.TagDetailView.as_view()),
    # JWT (Step 9)
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]