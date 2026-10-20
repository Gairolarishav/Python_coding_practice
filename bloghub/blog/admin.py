from django.contrib import admin
from .models import Category,Post,Tag,Comment

# Register your models here.
class CommentInline(admin.TabularInline):  # comments inside the post page
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "status", "views", "created_at"]
    list_filter = ["status", "created_at", "category"]
    search_fields = ["title", "body", "author__username"]
    prepopulated_fields = {"slug": ("title", )}
    filter_horizontal = ["tags"]
    list_select_related = ["author", "category"]
    inlines = [CommentInline]


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
