from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView
from .models import Post
from django.views import View
from django.db.models import F, Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView,DeleteView
from .forms import PostForm, CommentForm

# Create your views here.

# TemplateView: only shows a template
class AboutView(TemplateView):
    template_name = "blog/about.html"

# Plain View: you write get() / post() yourself (full control)
class PingView(View):
    def get(self,request):
        return HttpResponse("pong")

def post_list_fbv(request):
    posts = (
        Post.published
        .select_related("author", "category")   # ForeignKey / OneToOne -> uses SQL JOIN
        .prefetch_related("tags")
    )
    context = {"posts" : posts}   #2) Put in dictionary
    return render(request,"blog/post_list_fbv.html",context)  #3)pass to template

@login_required
def post_detail(request, slug):
    post = get_object_or_404(
        Post.published.select_related("author", "category").prefetch_related("tags","comments__author"),
        slug = slug ,   
    )

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request,"Comment added.")
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    # F(): +1 view directly in the database (safe, no race condition)
    Post.objects.filter(pk = post.pk).update(views=F("views") + 1)
    
    # Q(): OR condition -> same category OR shares a tag
    post.refresh_from_db(fields=["views"])

    related = (
        Post.published.filter(Q(category = post.category) | Q(tags__in = post.tags.all())).exclude(pk = post.pk).distinct()[:3]
    )

    return render(request, "blog/post_detail.html", {"post": post,"related":related, "form": form})




class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self,form):
        form.instance.author = self.request.user  # set author automatically
        messages.success(self.request, "Post Created!")
        return super().form_valid(form)   # saves + redirects to get_absolute_url

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



from .services import get_quote

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        qs = (
            Post.published
                .select_related(
                "author", "category")
                .prefetch_related("tags")
                # annotate: add a calculated column to every post
                .annotate(comment_count = Count("comments"),filter=Q(comments__active=True))
        )

        q = self.request.GET.get("q")

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(body__icontains= q) | Q(author__username__icontains=q))

        return qs


    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q","")
        context["quote"] = get_quote()  # third-party API
        return context


from django.db.models import Sum,Avg,Max
from accounts.models import User
from .models import Category

def stats(request):
    # agrregate: One result for whole table
    totals =  Post.published.aggregate(
        total_posts = Count("id"),
        total_views = Sum("views"),
        avg_views = Avg("views"),
        max_views = Max("views"),
    )

    # annotate: a calculated value for each row
    top_authors = (
        User.objects.annotate(
            post_count = Count("posts", filter=Q(posts__status= "published")))
            .filter(post_count__gt = 0).order_by("-post_count")[:5]
    )

    categories = Category.objects.annotate(n= Count("posts")).order_by("-n")
    most_commented = Post.published.annotate(c= Count("comments")).order_by("-c")[:5]


    # F in filter: compare two columns of the same row
    edited = Post.published.filter(updated_at__gt=F("created_at")).count()

    return render(request, "blog/stats.html", {
        "totals": totals, "top_authors": top_authors, "categories": categories,
        "most_commented": most_commented, "edited": edited,
    })

    

    
