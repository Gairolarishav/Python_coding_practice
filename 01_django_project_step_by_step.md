# Django — Build ONE Project Step by Step (BlogHub)

We build one small blog called **BlogHub**. Every topic you listed is used inside it.

**What BlogHub does:** users register and log in, write posts with an image, comment, search, see stats. The home page shows a "quote of the day" from a third-party API.

## Where each topic is covered

| Topic | Step |
|---|---|
| Project, app, register app | 3, 4, 5 |
| PostgreSQL | 2, 5 |
| Static and media | 5, 12, 23 |
| Custom user | 6 |
| Models, ForeignKey, OneToOne, ManyToMany, `class Meta`, indexing | 6, 7 |
| Custom manager | 7 |
| Admin panel | 9 |
| URLs and `include` | 11 |
| Templates, `extends`, `include` | 12 |
| Function views | 13, 15 |
| `select_related`, `prefetch_related` | 14 |
| Class views, generic views | 16, 17, 19 |
| Forms and validation | 18 |
| Authentication | 20 |
| Sessions | 22 |
| Signals | 24 |
| Middleware | 25 |
| Third-party API | 26 |
| `aggregate`, `annotate`, `F`, `Q`, `only`, `defer` | 15, 17, 27 |

## Final folder structure

```
bloghub/
├── manage.py
├── config/                  # project (settings.py, urls.py)
├── accounts/                # custom user, profile, register
│   └── models.py admin.py forms.py views.py urls.py signals.py apps.py
├── blog/                    # posts, comments
│   └── models.py admin.py forms.py views.py urls.py signals.py middleware.py services.py apps.py
├── templates/
│   ├── base.html
│   ├── partials/navbar.html
│   ├── partials/post_card.html
│   ├── blog/   (post_list, post_list_fbv, post_detail, post_form, post_confirm_delete, about, stats)
│   ├── accounts/ (login, register)
├── static/css/style.css
└── media/                   # created automatically on first upload
```

---

# PART 1 — SETUP

## Step 1 — Folder, virtual environment, packages

**Why:** a virtual environment keeps this project's packages separate from other projects.

```bash
mkdir bloghub && cd bloghub
python -m venv venv
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows

pip install django psycopg2-binary pillow requests
```

- `psycopg2-binary` → Django talks to PostgreSQL
- `pillow` → needed for image upload (`ImageField`)
- `requests` → to call the third-party API

---

## Step 2 — Create the PostgreSQL database

```bash
psql -U postgres
```
```sql
CREATE DATABASE bloghub;
\q
```

---

## Step 3 — Create the project

**Why:** the *project* holds settings and main URLs. *Apps* hold features.

```bash
django-admin startproject config .
```

The `.` means "create here, don't make an extra folder".

Test: `python manage.py runserver` → open http://127.0.0.1:8000 → rocket page. Stop with `Ctrl + C`.

---

## Step 4 — Create the apps

```bash
python manage.py startapp accounts
python manage.py startapp blog
```

- `accounts` = user related things
- `blog` = posts and comments

---

## Step 5 — Settings (register apps, database, templates, static, media)

Open `config/settings.py` and change these parts.

**1) Register the apps**

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",      # sessions
    "django.contrib.messages",
    "django.contrib.staticfiles",   # static files

    "accounts.apps.AccountsConfig", # our apps
    "blog.apps.BlogConfig",
]
```

**2) Custom user (must be done BEFORE the first migrate)**

```python
AUTH_USER_MODEL = "accounts.User"
```

**3) PostgreSQL**

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "bloghub",
        "USER": "postgres",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

**4) Templates folder** (add `BASE_DIR / "templates"` to `DIRS`)

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

**5) Static and media**

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]      # your own css/js/images

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"               # user uploads go here
```

- **Static** = files you write (CSS, JS, logo).
- **Media** = files users upload (post images, avatars).

**6) Login settings**

```python
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "post_list"
LOGOUT_REDIRECT_URL = "post_list"
```

Create the folders:

```bash
mkdir templates static static/css
```

---

# PART 2 — MODELS

## Step 6 — Custom User + Profile (`accounts/models.py`)

**Why custom user:** later you can add fields (email login, phone, etc.) without pain.

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)      # make email unique


class Profile(models.Model):
    # OneToOne = one user has exactly one profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.username
```

- `AbstractUser` already gives username, password, first_name, etc.
- `related_name="profile"` → `user.profile` gives the profile.
- `on_delete=CASCADE` → delete user → profile is deleted too.

---

## Step 7 — Blog models (`blog/models.py`)

```python
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# ---------- Custom manager ----------
class PublishedManager(models.Manager):
    """Post.published.all() returns only published posts."""
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"   # admin shows "categories" not "categorys"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [("draft", "Draft"), ("published", "Published")]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True, null=True)

    # ForeignKey = many posts -> one user
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    # many posts -> one category (keep post if category deleted)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    # ManyToMany = a post has many tags, a tag has many posts
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()        # default manager (all posts)
    published = PublishedManager()    # custom manager (only published)

    class Meta:
        ordering = ["-created_at"]    # newest first
        indexes = [
            # speeds up: filter(status=...).order_by("-created_at")
            models.Index(fields=["status", "-created_at"], name="post_status_created_idx"),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug, n = base, 1
            while Post.objects.filter(slug=slug).exists():   # keep slug unique
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author} on {self.post}"
```

**Quick notes**

- `related_name` = the name used for the reverse direction: `user.posts.all()`, `post.comments.all()`.
- `class Meta` = extra settings of the model (ordering, indexes, plural name).
- An **index** makes searching on those columns faster (like the index of a book).
- Use `Post.published.all()` for public pages and `Post.objects.all()` when you need everything.

---

## Step 8 — Migrations

**Why:** migrations turn your Python models into real database tables.

```bash
python manage.py makemigrations
python manage.py migrate
```

- `makemigrations` = writes the plan
- `migrate` = runs the plan on PostgreSQL

---

## Step 9 — Admin panel

**`accounts/admin.py`**

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


class ProfileInline(admin.StackedInline):    # edit profile inside the user page
    model = Profile
    can_delete = False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ["username", "email", "is_staff"]
```

**`blog/admin.py`**

```python
from django.contrib import admin
from .models import Category, Tag, Post, Comment


class CommentInline(admin.TabularInline):    # comments inside the post page
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "status", "views", "created_at"]
    list_filter = ["status", "category", "created_at"]
    search_fields = ["title", "body", "author__username"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]             # nice widget for ManyToMany
    list_select_related = ["author", "category"]
    inlines = [CommentInline]


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
```

---

## Step 10 — Superuser and sample data

```bash
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/admin/ → log in → add:
1. 2 categories, 3 tags
2. 5–8 posts with `status = Published` (some with an image)
3. A few comments

---

# PART 3 — URLS, TEMPLATES, VIEWS

## Step 11 — URLs and `include`

**Why:** each app has its own `urls.py`; the project `urls.py` just *includes* them.

**`config/urls.py`**

```python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),   # include = plug in app urls
    path("", include("blog.urls")),
]

# show uploaded media files while developing
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Create `blog/urls.py`** (we will fill it as we go):

```python
from django.urls import path
from . import views

urlpatterns = [
    path("fbv/", views.post_list_fbv, name="post_list_fbv"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
]
```

**Create `accounts/urls.py`** (empty for now):

```python
urlpatterns = []
```

---

## Step 12 — Templates: `extends`, `include`, static

**Idea:** write the common layout ONCE in `base.html`; other pages extend it.

**`templates/base.html`**

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}BlogHub{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
  {% include "partials/navbar.html" %}

  {% if messages %}
    {% for m in messages %}<div class="msg {{ m.tags }}">{{ m }}</div>{% endfor %}
  {% endif %}

  <main class="container">
    {% block content %}{% endblock %}
  </main>
</body>
</html>
```

**`templates/partials/navbar.html`** (`include` = reuse a small piece)

```html
<nav class="nav">
  <a href="{% url 'post_list' %}">BlogHub</a>
  <a href="{% url 'about' %}">About</a>
  <a href="{% url 'stats' %}">Stats</a>
  <span class="spacer"></span>
  {% if user.is_authenticated %}
    <a href="{% url 'post_create' %}">New Post</a>
    <span>Hi, {{ user.username }}</span>
    <form method="post" action="{% url 'logout' %}" style="display:inline">
      {% csrf_token %}<button>Logout</button>
    </form>
  {% else %}
    <a href="{% url 'login' %}">Login</a>
    <a href="{% url 'register' %}">Register</a>
  {% endif %}
</nav>
```

**`templates/partials/post_card.html`**

```html
<article class="card">
  {% if post.image %}<img src="{{ post.image.url }}" alt="{{ post.title }}">{% endif %}
  <h3><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h3>
  <p class="small">
    by {{ post.author.username }}
    {% if post.category %}| {{ post.category.name }}{% endif %}
    | {{ post.created_at|date:"d M Y" }} | {{ post.views }} views
  </p>
  <p>{{ post.body|truncatewords:25 }}</p>
  {% for tag in post.tags.all %}<span class="tag">#{{ tag.name }}</span>{% endfor %}
</article>
```

**`static/css/style.css`**

```css
body { font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }
.nav { display: flex; gap: 15px; align-items: center; background: #222; padding: 12px 20px; }
.nav a, .nav span { color: #fff; text-decoration: none; }
.spacer { flex: 1; }
.container { max-width: 800px; margin: 20px auto; padding: 0 15px; }
.card { background: #fff; padding: 15px; margin-bottom: 15px; border-radius: 6px; }
.card img { max-width: 100%; max-height: 250px; }
.small { color: #777; font-size: 13px; }
.tag { background: #e0e0e0; padding: 2px 8px; border-radius: 10px; font-size: 12px; margin-right: 4px; }
.msg { padding: 10px; background: #d4edda; text-align: center; }
.msg.error { background: #f8d7da; }
.errorlist { color: red; padding-left: 15px; }
```

---

## Step 13 — First view: Function-Based View (FBV)

**Flow:** URL → view → fetch data from DB → pass data in a dictionary → template.

**`blog/views.py`**

```python
from django.shortcuts import render
from .models import Post


def post_list_fbv(request):
    posts = Post.published.all()                       # 1) fetch data
    context = {"posts": posts}                         # 2) put in dictionary
    return render(request, "blog/post_list_fbv.html", context)   # 3) pass to template
```

**`templates/blog/post_list_fbv.html`**

```html
{% extends "base.html" %}
{% block title %}Posts (FBV){% endblock %}

{% block content %}
  <h1>All Posts (function view)</h1>
  {% for post in posts %}
    {% include "partials/post_card.html" %}
  {% empty %}
    <p>No posts yet.</p>
  {% endfor %}
{% endblock %}
```

Temporarily add the missing URL names so the navbar doesn't crash — we will add real ones in later steps. For now just open http://127.0.0.1:8000/fbv/ **after Step 17** (navbar needs all url names). If you want to test right now, remove the navbar `{% url %}` lines temporarily.

---

## Step 14 — Fix the N+1 problem: `select_related` and `prefetch_related`

**Problem:** the card shows `post.author` and `post.tags`. Without help, Django runs **one extra query per post** (slow).

**Fix:**

```python
def post_list_fbv(request):
    posts = (
        Post.published
        .select_related("author", "category")   # ForeignKey / OneToOne -> uses SQL JOIN
        .prefetch_related("tags")               # ManyToMany / reverse FK -> 2nd query, joins in Python
    )
    return render(request, "blog/post_list_fbv.html", {"posts": posts})
```

| | Use for | How |
|---|---|---|
| `select_related` | ForeignKey, OneToOne | one query with JOIN |
| `prefetch_related` | ManyToMany, reverse FK (`post.comments`) | one extra query, merged in Python |

---

## Step 15 — Detail page (FBV) with `F()` and `Q()`

Add to `blog/views.py`:

```python
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, render


def post_detail(request, slug):
    post = get_object_or_404(
        Post.published.select_related("author", "category").prefetch_related("tags", "comments__author"),
        slug=slug,
    )

    # F(): +1 view directly in the database (safe, no race condition)
    Post.objects.filter(pk=post.pk).update(views=F("views") + 1)
    post.refresh_from_db(fields=["views"])

    # Q(): OR condition -> same category OR shares a tag
    related = (
        Post.published
        .filter(Q(category=post.category) | Q(tags__in=post.tags.all()))
        .exclude(pk=post.pk)
        .distinct()[:3]
    )

    return render(request, "blog/post_detail.html", {"post": post, "related": related})
```

**`templates/blog/post_detail.html`**

```html
{% extends "base.html" %}
{% block title %}{{ post.title }}{% endblock %}

{% block content %}
  <article class="card">
    <h1>{{ post.title }}</h1>
    <p class="small">by {{ post.author.username }} | {{ post.created_at|date:"d M Y" }} | {{ post.views }} views</p>
    {% if post.image %}<img src="{{ post.image.url }}" alt="">{% endif %}
    <p>{{ post.body|linebreaks }}</p>

    {% if user == post.author %}
      <a href="{% url 'post_update' post.slug %}">Edit</a> |
      <a href="{% url 'post_delete' post.slug %}">Delete</a>
    {% endif %}
  </article>

  <h3>Comments ({{ post.comments.all|length }})</h3>
  {% for c in post.comments.all %}
    <div class="card"><b>{{ c.author.username }}</b>: {{ c.text }}</div>
  {% empty %}
    <p>No comments yet.</p>
  {% endfor %}

  {# comment form is added in Step 21 #}

  {% if related %}
    <h3>Related posts</h3>
    {% for post in related %}{% include "partials/post_card.html" %}{% endfor %}
  {% endif %}
{% endblock %}
```

---

## Step 16 — Class-Based Views: `TemplateView` and `View`

**Why:** a class-based view (CBV) is a class instead of a function. Less repeated code.

Add to `blog/views.py`:

```python
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse


# TemplateView: only shows a template
class AboutView(TemplateView):
    template_name = "blog/about.html"


# Plain View: you write get() / post() yourself (full control)
class PingView(View):
    def get(self, request):
        return HttpResponse("pong")
```

**`templates/blog/about.html`**

```html
{% extends "base.html" %}
{% block content %}
  <h1>About BlogHub</h1>
  <p>A small blog built with Django.</p>
{% endblock %}
```

---

## Step 17 — Generic View: `ListView` (search, `annotate`, pagination)

**Generic views** = ready-made classes for common jobs (list, detail, create, update, delete).

Add to `blog/views.py`:

```python
from django.db.models import Count, Q
from django.views.generic import ListView
from .services import get_quote


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        qs = (
            Post.published
            .select_related("author", "category")
            .prefetch_related("tags")
            # annotate: add a calculated column to every post
            .annotate(comment_count=Count("comments", filter=Q(comments__active=True)))
        )
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(body__icontains=q) | Q(author__username__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        context["quote"] = get_quote()             # third-party API (Step 26)
        return context
```

For now create a temporary `blog/services.py` so it runs:

```python
def get_quote():
    return None
```

**`templates/blog/post_list.html`**

```html
{% extends "base.html" %}
{% block title %}Home{% endblock %}

{% block content %}
  {% if quote %}
    <div class="card"><i>"{{ quote.text }}"</i> — {{ quote.author }}</div>
  {% endif %}

  <form method="get">
    <input name="q" value="{{ q }}" placeholder="Search posts...">
    <button>Search</button>
  </form>

  {% for post in posts %}
    {% include "partials/post_card.html" %}
    <p class="small">💬 {{ post.comment_count }} comments</p>
  {% empty %}
    <p>No posts found.</p>
  {% endfor %}

  {% if is_paginated %}
    <p>
      {% if page_obj.has_previous %}<a href="?page={{ page_obj.previous_page_number }}&q={{ q }}">Prev</a>{% endif %}
      Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
      {% if page_obj.has_next %}<a href="?page={{ page_obj.next_page_number }}&q={{ q }}">Next</a>{% endif %}
    </p>
  {% endif %}
{% endblock %}
```

**Update `blog/urls.py`** (full file so far):

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("fbv/", views.post_list_fbv, name="post_list_fbv"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("ping/", views.PingView.as_view(), name="ping"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
]
```

---

## Step 18 — Forms and validation

**`blog/forms.py`**

```python
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "image", "category", "tags", "status"]

    # field validation: method name must be clean_<fieldname>
    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters.")
        return title

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and hasattr(image, "size") and image.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Image must be smaller than 2 MB.")
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {"text": forms.Textarea(attrs={"rows": 3})}

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if len(text) < 3:
            raise forms.ValidationError("Comment is too short.")
        return text
```

**`accounts/forms.py`**

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already used.")
        return email
```

**Validation order:** field `clean_<name>()` → `clean()` (whole form) → errors shown in template automatically.

---

## Step 19 — Generic Create / Update / Delete views

Add to `blog/views.py`:

```python
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import PostForm


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user      # set author automatically
        messages.success(self.request, "Post created!")
        return super().form_valid(form)               # saves + redirects to get_absolute_url


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class PostUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"


class PostDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")
```

**`templates/blog/post_form.html`**

```html
{% extends "base.html" %}
{% block content %}
  <h1>{% if object %}Edit{% else %}New{% endif %} Post</h1>
  <form method="post" enctype="multipart/form-data">   {# enctype needed for file upload #}
    {% csrf_token %}
    {{ form.as_p }}
    <button>Save</button>
  </form>
{% endblock %}
```

**`templates/blog/post_confirm_delete.html`**

```html
{% extends "base.html" %}
{% block content %}
  <h1>Delete "{{ object.title }}"?</h1>
  <form method="post">{% csrf_token %}<button>Yes, delete</button></form>
  <a href="{{ object.get_absolute_url }}">Cancel</a>
{% endblock %}
```

**Add to `blog/urls.py`** (put `post/new/` BEFORE `post/<slug>/`):

```python
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
```

---

# PART 4 — USERS, SESSIONS, MEDIA

## Step 20 — Authentication: register, login, logout

**`accounts/views.py`**

```python
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)                      # log in right after registering
            messages.success(request, "Welcome to BlogHub!")
            return redirect("post_list")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})
```

**`accounts/urls.py`**

```python
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
```

**`templates/accounts/login.html`**

```html
{% extends "base.html" %}
{% block content %}
  <h1>Login</h1>
  <form method="post">{% csrf_token %}{{ form.as_p }}<button>Login</button></form>
  <p>No account? <a href="{% url 'register' %}">Register</a></p>
{% endblock %}
```

**`templates/accounts/register.html`**

```html
{% extends "base.html" %}
{% block content %}
  <h1>Register</h1>
  <form method="post">{% csrf_token %}{{ form.as_p }}<button>Create account</button></form>
{% endblock %}
```

**Protect function views:**

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request): ...
```

(For class views we used `LoginRequiredMixin`.)

Run the server → try register, logout, login.

---

## Step 21 — Comment form on the detail page

In `blog/views.py` update `post_detail`:

```python
from django.contrib import messages
from django.shortcuts import redirect
from .forms import CommentForm


def post_detail(request, slug):
    post = get_object_or_404(
        Post.published.select_related("author", "category").prefetch_related("tags", "comments__author"),
        slug=slug,
    )

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)     # don't save yet
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added.")
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    Post.objects.filter(pk=post.pk).update(views=F("views") + 1)
    post.refresh_from_db(fields=["views"])

    related = (
        Post.published.filter(Q(category=post.category) | Q(tags__in=post.tags.all()))
        .exclude(pk=post.pk).distinct()[:3]
    )
    return render(request, "blog/post_detail.html", {"post": post, "related": related, "form": form})
```

In `post_detail.html`, replace the comment `{# ... #}` line with:

```html
  {% if user.is_authenticated %}
    <form method="post">{% csrf_token %}{{ form.as_p }}<button>Add comment</button></form>
  {% else %}
    <p><a href="{% url 'login' %}">Login</a> to comment.</p>
  {% endif %}
```

---

## Step 22 — Sessions: "Recently viewed posts"

**Session** = data stored on the server for each visitor (the browser only holds a session id cookie).

In `post_detail`, right after the `get_object_or_404`, add:

```python
    viewed = request.session.get("recent", [])
    if post.pk in viewed:
        viewed.remove(post.pk)
    viewed.insert(0, post.pk)
    request.session["recent"] = viewed[:5]      # keep last 5
```

Show them on the home page. In `PostListView.get_context_data` add:

```python
        ids = self.request.session.get("recent", [])
        posts_by_id = {p.pk: p for p in Post.published.filter(pk__in=ids).only("title", "slug")}
        context["recent"] = [posts_by_id[i] for i in ids if i in posts_by_id]
```

In `post_list.html` (above the search form):

```html
  {% if recent %}
    <div class="card"><b>Recently viewed:</b>
      {% for p in recent %}<a href="{{ p.get_absolute_url }}">{{ p.title }}</a>{% if not forloop.last %} · {% endif %}{% endfor %}
    </div>
  {% endif %}
```

(Login itself also uses sessions — that is how Django remembers you are logged in.)

---

## Step 23 — Media files (upload and show images)

Already done in earlier steps. Checklist:

1. `MEDIA_URL` / `MEDIA_ROOT` in settings ✅ (Step 5)
2. `static(settings.MEDIA_URL, ...)` in `config/urls.py` ✅ (Step 11)
3. `ImageField(upload_to="posts/")` ✅ (Step 7)
4. `enctype="multipart/form-data"` on the form ✅ (Step 19)
5. `{{ post.image.url }}` in template ✅ (Step 12)

Create a post with an image → file appears in `media/posts/`.

---

# PART 5 — SIGNALS, MIDDLEWARE, THIRD-PARTY API

## Step 24 — Signals

**Signal** = "when X happens, automatically run this function".

**1) Auto-create a Profile when a user is created — `accounts/signals.py`**

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

**2) Log when a comment is added — `blog/signals.py`**

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment


@receiver(post_save, sender=Comment)
def comment_added(sender, instance, created, **kwargs):
    if created:
        print(f"[signal] New comment by {instance.author} on '{instance.post}'")
```

**3) Connect them — `accounts/apps.py` and `blog/apps.py`**

```python
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from . import signals      # noqa  (this line makes signals work)
```

Do the same in `blog/apps.py` (class `BlogConfig`, `name = "blog"`, import `signals`).

**Test:** register a new user → check admin → the Profile exists. Add a comment → see the print in the terminal.

---

## Step 25 — Middleware

**Middleware** = code that runs on EVERY request/response, before and after the view.

**`blog/middleware.py`**

```python
import time


class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response          # runs once at server start

    def __call__(self, request):
        start = time.time()                       # BEFORE the view

        response = self.get_response(request)     # the view runs here

        ms = (time.time() - start) * 1000         # AFTER the view
        response["X-Time-Ms"] = f"{ms:.1f}"
        print(f"[middleware] {request.method} {request.path} -> {response.status_code} ({ms:.1f} ms)")
        return response
```

**Add to `MIDDLEWARE` in settings (at the end):**

```python
MIDDLEWARE = [
    # ... default ones ...
    "blog.middleware.RequestTimingMiddleware",
]
```

Open any page → see the log line in the terminal.

---

## Step 26 — Third-party API integration

We call a free quotes API (`https://zenquotes.io/api/random`) and show the quote on the home page.

**`blog/services.py`** (replace the temporary one)

```python
import requests
from django.core.cache import cache


def get_quote():
    quote = cache.get("quote_of_the_day")          # reuse for 1 hour (don't spam the API)
    if quote:
        return quote
    try:
        r = requests.get("https://zenquotes.io/api/random", timeout=5)
        r.raise_for_status()
        data = r.json()[0]                         # [{"q": "...", "a": "..."}]
        quote = {"text": data["q"], "author": data["a"]}
        cache.set("quote_of_the_day", quote, 60 * 60)
        return quote
    except (requests.RequestException, KeyError, IndexError, ValueError):
        return None                                # if API is down, site still works
```

Rules for any API call: always use `timeout`, always handle errors, cache the result.

`PostListView` already passes `quote` to the template (Step 17) → refresh home page to see it.

---

# PART 6 — QUERY SKILLS

## Step 27 — Stats page + Query Lab

**Stats view — add to `blog/views.py`:**

```python
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, F, Max, Q, Sum
from django.shortcuts import render
from .models import Category

User = get_user_model()


def stats(request):
    # aggregate: ONE result for the whole table
    totals = Post.published.aggregate(
        total_posts=Count("id"),
        total_views=Sum("views"),
        avg_views=Avg("views"),
        max_views=Max("views"),
    )

    # annotate: a calculated value for EACH row
    top_authors = (
        User.objects
        .annotate(post_count=Count("posts", filter=Q(posts__status="published")))
        .filter(post_count__gt=0)
        .order_by("-post_count")[:5]
    )
    categories = Category.objects.annotate(n=Count("posts")).order_by("-n")
    most_commented = Post.published.annotate(c=Count("comments")).order_by("-c")[:5]

    # F in filter: compare two columns of the same row
    edited = Post.published.filter(updated_at__gt=F("created_at")).count()

    return render(request, "blog/stats.html", {
        "totals": totals, "top_authors": top_authors, "categories": categories,
        "most_commented": most_commented, "edited": edited,
    })
```

**`templates/blog/stats.html`**

```html
{% extends "base.html" %}
{% block content %}
  <h1>Stats</h1>
  <div class="card">
    Posts: {{ totals.total_posts }} | Views: {{ totals.total_views }} |
    Average: {{ totals.avg_views|floatformat:1 }} | Max: {{ totals.max_views }} |
    Edited posts: {{ edited }}
  </div>

  <h3>Top authors</h3>
  <ul>{% for a in top_authors %}<li>{{ a.username }} — {{ a.post_count }} posts</li>{% endfor %}</ul>

  <h3>Posts per category</h3>
  <ul>{% for c in categories %}<li>{{ c.name }} — {{ c.n }}</li>{% endfor %}</ul>

  <h3>Most commented</h3>
  <ul>{% for p in most_commented %}<li>{{ p.title }} — {{ p.c }}</li>{% endfor %}</ul>
{% endblock %}
```

**Add URL:** `path("stats/", views.stats, name="stats"),`

### Query Lab — try in the shell

```bash
python manage.py shell
```

```python
from django.db.models import Count, F, Q
from blog.models import Post, Category, Tag
from django.contrib.auth import get_user_model
User = get_user_model()

# only(): load ONLY these columns
Post.objects.only("title", "slug")

# defer(): load everything EXCEPT these columns
Post.objects.defer("body")
# warning: using a deferred field later runs 1 extra query per object

# values / values_list: dictionaries or tuples instead of objects
Post.objects.values("title", "views")
Post.objects.values_list("title", flat=True)

# F: update using the column's own value
Post.objects.filter(status="published").update(views=F("views") + 10)

# Q: OR, AND, NOT
Post.objects.filter(Q(title__icontains="django") | Q(views__gt=100))
Post.objects.filter(~Q(status="draft"))

# annotate + filter
Post.objects.annotate(c=Count("comments")).filter(c__gte=2)

# relations
user = User.objects.first()
user.posts.all()                      # reverse ForeignKey (related_name="posts")
user.profile                          # OneToOne
post = Post.objects.first()
post.tags.all()                       # ManyToMany
post.tags.add(Tag.objects.first())    # add a tag
post.comments.count()
Category.objects.first().posts.all()

# lazy queries: SQL runs only when you use the data
qs = Post.objects.filter(status="published")   # no SQL yet
list(qs)                                       # SQL runs now

# see the SQL
print(Post.objects.filter(status="published").query)
```

---

# FINAL CHECK

```bash
python manage.py runserver
```

- [ ] Register → logged in → Profile created (signal)
- [ ] Create a post with an image → appears on home
- [ ] Search works, pagination works
- [ ] Open a post → views +1, comment works
- [ ] Recently viewed list appears (session)
- [ ] Only the author sees Edit / Delete
- [ ] Quote of the day shows (API)
- [ ] Terminal shows middleware timing lines
- [ ] `/stats/` works
- [ ] `/admin/` works

## Common errors

| Error | Fix |
|---|---|
| `NoReverseMatch` | URL name missing in `urls.py` — check `name=` |
| `TemplateDoesNotExist` | Check `DIRS` in settings and file path |
| `relation "accounts_user" does not exist` | Set `AUTH_USER_MODEL` first, drop DB, migrate again |
| Images not showing | Check `MEDIA_URL`, the `static()` line in urls, and `DEBUG=True` |
| `CSRF verification failed` | Add `{% csrf_token %}` inside the form |
| `Pillow` error | `pip install pillow` |
| Signal not running | Add `ready()` and use `AccountsConfig` in `INSTALLED_APPS` |

**Next:** open `02_drf_project_step_by_step.md` — we add REST APIs to this same project.
