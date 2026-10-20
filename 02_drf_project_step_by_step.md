# Django REST Framework — Add APIs to the SAME Project (BlogHub)

Finish `01_django_project_step_by_step.md` first. Here we keep the same models and add a **REST API** on top.

**What is an API?** A URL that returns **JSON** (data) instead of an HTML page. Mobile apps and React/Vue apps use it.

## Where each topic is covered

| Topic | Step |
|---|---|
| Install + settings | 1, 2 |
| Serializers (Model, nested, method field, validation) | 3 |
| Function API (`@api_view`) | 4 |
| Class API (`APIView`) | 5 |
| Generic API views | 6 |
| ViewSet + Router + custom actions | 7 |
| Permissions (built-in + custom) | 8 |
| Authentication (Token / JWT) + Register | 9 |
| Filter, search, order, pagination | 10 |
| Throttling | 11 |
| Image upload | 12 |
| Aggregate / annotate in API, third-party API | 13 |
| Testing | 14, 15 |

## New files we will create

```
api/
├── serializers.py
├── permissions.py
├── views.py
└── urls.py
```

## The API we are building

| Method | URL | What it does |
|---|---|---|
| POST | `/api/register/` | create account |
| POST | `/api/token/` | login → get JWT |
| GET | `/api/me/` | my info |
| GET | `/api/posts/` | list posts (search, filter, page) |
| POST | `/api/posts/` | create post (login needed) |
| GET | `/api/posts/<slug>/` | one post |
| PUT/PATCH/DELETE | `/api/posts/<slug>/` | only the owner |
| POST | `/api/posts/<slug>/comment/` | add a comment |
| GET | `/api/posts/mine/` | my posts |
| GET | `/api/posts/stats/` | totals |
| GET | `/api/categories/` | categories |
| GET | `/api/quote/` | quote from third-party API |

---

# PART 1 — SETUP

## Step 1 — Install and create the `api` app

```bash
pip install djangorestframework django-filter djangorestframework-simplejwt
python manage.py startapp api
```

- `djangorestframework` = DRF
- `django-filter` = easy filtering (`?category=1`)
- `simplejwt` = JWT login

---

## Step 2 — Settings

**`config/settings.py`**

```python
INSTALLED_APPS = [
    # ... django apps ...
    "rest_framework",
    "django_filters",

    "accounts.apps.AccountsConfig",
    "blog.apps.BlogConfig",
    "api",
]

REST_FRAMEWORK = {
    # who are you? (authentication)
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",   # lets the browsable API work after admin login
    ],
    # what can you do? (permission)
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    # pagination
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,
    # filtering
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    # throttling (Step 11)
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "30/min", "user": "120/min"},
}
```

**Authentication vs Permission:**
- Authentication = *who are you?* (token, session)
- Permission = *are you allowed to do this?*

---

# PART 2 — SERIALIZERS

## Step 3 — Serializers (`api/serializers.py`)

**Serializer** = translator.
- Model object → JSON (output)
- JSON → validated data → model object (input)

```python
from django.contrib.auth import get_user_model
from rest_framework import serializers
from blog.models import Category, Tag, Post, Comment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)    # shows username

    class Meta:
        model = Comment
        fields = ["id", "author", "text", "created_at"]
        read_only_fields = ["id", "created_at"]


# ---------- READ serializer (output): nested data ----------
class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()                  # "ali"
    category = CategorySerializer(read_only=True)              # nested object
    tags = TagSerializer(many=True, read_only=True)            # nested list
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()        # custom calculated field

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "body", "image", "author", "category", "tags",
            "status", "views", "comment_count", "comments", "created_at",
        ]

    def get_comment_count(self, obj):                          # name must be get_<field>
        return obj.comments.count()


# ---------- WRITE serializer (input): ids only ----------
class PostWriteSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=False
    )

    class Meta:
        model = Post
        fields = ["title", "body", "image", "category", "tags", "status"]

    # field validation: validate_<fieldname>
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters.")
        return value

    # object validation: validate()
    def validate(self, data):
        if data.get("status") == "published" and len(data.get("body", "")) < 20:
            raise serializers.ValidationError("Published post needs a body of 20+ characters.")
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)   # never sent back

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already used.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)    # hashes the password


class MeSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(source="posts.count", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "post_count"]
```

**Key ideas**
- `read_only=True` → only in output. `write_only=True` → only in input.
- `source="posts.count"` → take the value from another attribute.
- Two serializers for Post (read vs write) keeps things clean.

---

# PART 3 — VIEWS (4 ways, from simple to powerful)

## Step 4 — Function-based API view (`@api_view`)

**`api/views.py`** — start with this:

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from blog.models import Category
from .serializers import CategorySerializer


@api_view(["GET", "POST"])
def category_list(request):
    if request.method == "GET":
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response(serializer.data)

    serializer = CategorySerializer(data=request.data)      # POST: JSON -> validate
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

---

## Step 5 — Class-based `APIView`

```python
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from blog.models import Tag
from .serializers import TagSerializer


class TagListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(TagSerializer(Tag.objects.all(), many=True).data)

    def post(self, request):
        s = TagSerializer(data=request.data)
        s.is_valid(raise_exception=True)        # auto-returns 400 with errors
        s.save()
        return Response(s.data, status=201)


class TagDetailView(APIView):
    def get(self, request, pk):
        return Response(TagSerializer(get_object_or_404(Tag, pk=pk)).data)

    def delete(self, request, pk):
        get_object_or_404(Tag, pk=pk).delete()
        return Response(status=204)
```

`APIView` = you write `get/post/put/delete` yourself.

---

## Step 6 — Generic API views (less code)

Ready-made classes: `ListAPIView`, `CreateAPIView`, `RetrieveAPIView`, `ListCreateAPIView`, `RetrieveUpdateDestroyAPIView` …

```python
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, MeSerializer

User = get_user_model()


class CategoryListCreate(generics.ListCreateAPIView):     # GET list + POST create
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None                               # categories are few, no paging


class RegisterView(generics.CreateAPIView):               # POST only
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MeView(generics.RetrieveAPIView):                   # GET only
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user                          # no <pk> needed
```

(Add `from rest_framework.permissions import IsAuthenticated` at the top.)

---

## Step 7 — ViewSet + Router (the main API)

**ViewSet** = one class that handles list, create, retrieve, update, delete. The **Router** builds the URLs automatically.

First write the custom permission.

**`api/permissions.py`**

```python
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Anyone can read. Only the author can edit/delete."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:     # GET, HEAD, OPTIONS
            return True
        return obj.author == request.user
```

Now the ViewSet in **`api/views.py`**:

```python
from django.db.models import Avg, Count, Q, Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from blog.models import Post
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    PostSerializer, PostWriteSerializer, CommentSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = "slug"                                   # /posts/<slug>/ instead of id

    # filtering / search / ordering (Step 10)
    filterset_fields = ["category", "tags", "author", "status"]
    search_fields = ["title", "body", "author__username"]
    ordering_fields = ["created_at", "views", "title"]

    # 1) queryset: per-user filtering + fast queries
    def get_queryset(self):
        qs = (
            Post.objects
            .select_related("author", "category")
            .prefetch_related("tags", "comments__author")
            .annotate(comment_total=Count("comments"))
        )
        user = self.request.user
        if user.is_authenticated:
            return qs.filter(Q(status="published") | Q(author=user))   # published + my drafts
        return qs.filter(status="published")

    # 2) different serializer for different actions
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PostWriteSerializer
        return PostSerializer

    # 3) set author automatically when saving
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # ---------- custom actions ----------
    # POST /api/posts/<slug>/comment/
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def comment(self, request, slug=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, author=request.user)
        return Response(serializer.data, status=201)

    # GET /api/posts/mine/
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def mine(self, request):
        qs = self.filter_queryset(self.get_queryset().filter(author=request.user))
        page = self.paginate_queryset(qs)
        serializer = PostSerializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

    # GET /api/posts/stats/   (aggregate)
    @action(detail=False, methods=["get"])
    def stats(self, request):
        data = Post.published.aggregate(
            total_posts=Count("id"),
            total_views=Sum("views"),
            avg_views=Avg("views"),
        )
        return Response(data)
```

**Why `perform_create`?** The client should not send `author` — we take it from `request.user`.

| Class | Gives you |
|---|---|
| `ViewSet` | nothing ready, you write every action |
| `ModelViewSet` | list, create, retrieve, update, partial_update, destroy |
| `ReadOnlyModelViewSet` | list, retrieve only |

**Third-party API endpoint** (reuses `blog/services.py` from Django Step 26):

```python
from blog.services import get_quote


class QuoteView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        quote = get_quote()
        if quote is None:
            return Response({"detail": "Quote service unavailable."}, status=503)
        return Response(quote)
```

**`api/urls.py`**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register("posts", views.PostViewSet, basename="post")   # basename needed: we override get_queryset

urlpatterns = [
    path("", include(router.urls)),

    path("register/", views.RegisterView.as_view()),
    path("me/", views.MeView.as_view()),
    path("categories/", views.CategoryListCreate.as_view()),
    path("quote/", views.QuoteView.as_view()),

    # practice views from steps 4 and 5
    path("categories-fbv/", views.category_list),
    path("tags/", views.TagListView.as_view()),
    path("tags/<int:pk>/", views.TagDetailView.as_view()),

    # JWT (Step 9)
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]
```

**`config/urls.py`** — add one line:

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("api/", include("api.urls")),          # <-- new
    path("", include("blog.urls")),
]
```

Run `python manage.py runserver` and open http://127.0.0.1:8000/api/ — DRF shows a clickable page (Browsable API).

---

# PART 4 — SECURITY

## Step 8 — Permissions

| Permission | Meaning |
|---|---|
| `AllowAny` | everyone |
| `IsAuthenticated` | logged-in only |
| `IsAuthenticatedOrReadOnly` | everyone reads, login to write |
| `IsAdminUser` | staff only |
| custom `IsOwnerOrReadOnly` | author only can edit (Step 7) |

- **Where to set:** globally in settings (Step 2), or per view with `permission_classes = [...]`.
- **Two levels:**
  - `has_permission` → checked for the whole view
  - `has_object_permission` → checked for one object (used in detail/update/delete)
- Combine several: `permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]` → ALL must pass.

---

## Step 9 — Authentication (JWT)

**JWT flow:**
1. Client sends username + password to `/api/token/`
2. Server returns `access` (short life) and `refresh` (long life)
3. Client sends `Authorization: Bearer <access>` with each request
4. When `access` expires, send `refresh` to `/api/token/refresh/` to get a new one

**Optional token lifetime** (settings):

```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
```

**Try it (curl):**

```bash
# register
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"ali","email":"ali@test.com","password":"secret123"}'

# login -> returns access + refresh
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"ali","password":"secret123"}'

# use the access token
curl http://127.0.0.1:8000/api/me/ -H "Authorization: Bearer <ACCESS_TOKEN>"
```

Other options exist (Token auth, Session auth). JWT is the most common for mobile/SPA apps.

---

# PART 5 — EXTRA FEATURES

## Step 10 — Filtering, searching, ordering, pagination

Already switched on in Steps 2 and 7. Use them in the URL:

```
GET /api/posts/?search=django            # search in title, body, author
GET /api/posts/?category=1               # filter
GET /api/posts/?tags=2&author=1          # combine
GET /api/posts/?ordering=-views          # most viewed first
GET /api/posts/?page=2                   # next page
```

Paginated response looks like:

```json
{
  "count": 12,
  "next": "http://127.0.0.1:8000/api/posts/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

---

## Step 11 — Throttling (rate limit)

Already set in Step 2: anonymous = 30 requests/min, logged-in = 120/min. Too many requests → **HTTP 429**.

Special limit for one view:

```python
from rest_framework.throttling import ScopedRateThrottle

class QuoteView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "quote"
```

and in settings add `"quote": "5/min"` inside `DEFAULT_THROTTLE_RATES`.

---

## Step 12 — Image upload through the API

Because `PostWriteSerializer` has `image` in its fields, upload works with **multipart/form-data** (not JSON):

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -F "title=My first API post" \
  -F "body=This is the body of my post from the API." \
  -F "status=published" \
  -F "category=1" \
  -F "tags=1" -F "tags=2" \
  -F "image=@/path/to/photo.jpg"
```

The returned image URL is a full address (`http://127.0.0.1:8000/media/posts/photo.jpg`) because the request is passed in the serializer context automatically by the ViewSet.

---

## Step 13 — Aggregate / annotate in the API (recap)

- `aggregate` → `/api/posts/stats/` (one summary result)
- `annotate` → `comment_total` in `PostViewSet.get_queryset()` (one value per post)
- `select_related` / `prefetch_related` → in `get_queryset()` (fast queries)
- third-party API → `/api/quote/`

Tip: to expose the annotated value, add to `PostSerializer`:

```python
comment_total = serializers.IntegerField(read_only=True)
```

(and you may remove `get_comment_count` — this version has no extra query per post).

---

# PART 6 — TEST EVERYTHING

## Step 14 — Manual test with curl / Postman

```bash
TOKEN=<ACCESS_TOKEN>

# list (public)
curl http://127.0.0.1:8000/api/posts/

# one post
curl http://127.0.0.1:8000/api/posts/my-first-api-post/

# create (JSON, no image)
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"Hello API","body":"Body text longer than twenty chars","status":"published"}'

# partial update
curl -X PATCH http://127.0.0.1:8000/api/posts/hello-api/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"Hello API v2"}'

# comment
curl -X POST http://127.0.0.1:8000/api/posts/hello-api/comment/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"text":"Nice post!"}'

# delete
curl -X DELETE http://127.0.0.1:8000/api/posts/hello-api/ -H "Authorization: Bearer $TOKEN"
```

**HTTP status codes to remember**

| Code | Meaning |
|---|---|
| 200 | OK |
| 201 | Created |
| 204 | Deleted (no content) |
| 400 | Bad data (validation error) |
| 401 | Not logged in |
| 403 | Logged in but not allowed |
| 404 | Not found |
| 429 | Too many requests |

---

## Step 15 — Automated tests (`api/tests.py`)

```python
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from blog.models import Post

User = get_user_model()


class PostApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("ali", "ali@test.com", "secret123")
        self.other = User.objects.create_user("sara", "sara@test.com", "secret123")
        self.post = Post.objects.create(
            title="First post", body="Some long body text here for the post",
            author=self.user, status="published",
        )

    def test_list_is_public(self):
        res = self.client.get("/api/posts/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 1)

    def test_create_needs_login(self):
        res = self.client.post("/api/posts/", {"title": "Hello world", "body": "x" * 30})
        self.assertEqual(res.status_code, 401)

    def test_create_works_when_logged_in(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(
            "/api/posts/",
            {"title": "Hello world", "body": "x" * 30, "status": "published"},
        )
        self.assertEqual(res.status_code, 201)

    def test_only_owner_can_delete(self):
        self.client.force_authenticate(self.other)
        res = self.client.delete(f"/api/posts/{self.post.slug}/")
        self.assertEqual(res.status_code, 403)

    def test_validation_error(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/posts/", {"title": "Hi", "body": "short"})
        self.assertEqual(res.status_code, 400)
```

Run:

```bash
python manage.py test api
```

---

# FINAL CHECK

- [ ] `/api/` browsable page opens
- [ ] Register → token → `/api/me/` works
- [ ] Anonymous can read posts but cannot create (401)
- [ ] Create post with and without image
- [ ] Other user cannot edit or delete your post (403)
- [ ] Search, filter, ordering, pagination work
- [ ] Comment action works
- [ ] `/api/posts/stats/` and `/api/quote/` work
- [ ] `python manage.py test api` passes

## Common errors

| Error | Fix |
|---|---|
| `basename` error when registering router | Add `basename="post"` (we override `get_queryset`) |
| 401 even with token | Header must be exactly `Authorization: Bearer <token>` |
| 403 CSRF error in browsable API | Log in through `/admin/` first (SessionAuthentication) |
| Image upload fails | Use `-F` multipart, not JSON |
| `Field 'id' expected a number` | In ViewSet using slug, set `lookup_field = "slug"` |
| Router URL `mine` / `stats` treated as a slug | Custom `detail=False` actions are registered before detail routes — make sure they use `@action(detail=False)` |

## Quick summary of the 4 view styles

| Style | Code amount | Use when |
|---|---|---|
| `@api_view` function | medium | tiny custom endpoint |
| `APIView` | medium | full control |
| Generic views | small | normal list/create/detail |
| `ModelViewSet` + Router | smallest | full CRUD for a model |
