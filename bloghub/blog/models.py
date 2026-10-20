from django.db import models
from django.utils.text import slugify
from accounts.models import User
from .managers import PublishedManager
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True,blank=True)

    class Meta:
        verbose_name_plural = "categories" #admin shows categories not categorys
        ordering = ["name"]

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    STATUS_CHOICES = [("draft", "Draft"), ("published", "Published")]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True,null=True)

    # ForeignKey = many posts -> one user
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="posts")

    # many posts -> One category(keep posts if category deleted)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, blank=True, related_name="posts")

    # ManyToMany -> a posts have many tag, a tag have many posts
    tags = models.ManyToManyField(Tag, blank=True,related_name="posts")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # Default manager(all posts)
    published = PublishedManager() # Custom manager(only published)

    class Meta:
        ordering = ["-created_at"]  # newest first
        indexes = [
            # speeds up: filter(status=...).order_by("-created_at")
            models.Index(fields=["status", "-created_at"], name="post_status_created_idx")
        ]

    def save(self,*args,**kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug, n = base, 1
            while Post.objects.filter(slug=slug).exists():   # keep slug unique
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug

        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug" : self.slug})


    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created_at"]
    def __str__(self):
        return f"{self.author} on {self.post}"
    
    
    
