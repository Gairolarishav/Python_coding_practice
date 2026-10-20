from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from blog.models import Category
from .serializers import CategorySerializer
from rest_framework import status


# Create your views here.
@api_view(["GET","POST"])
def category_list(request):
    if request.method == "GET":
        category = Category.objects.all()
        serializer = CategorySerializer(category,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from blog.models import Tag
from .serializers import TagSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny,IsAuthenticated

class TagListView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = TagSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagDetailView(APIView):
    permission_classes  = [IsAuthenticated]

    def get(self,request,pk):
       tag = get_object_or_404(Tag,pk=pk)
       serializer = TagSerializer(tag)
       return Response(serializer.data)

    def delete(self,request,pk):
        tag = get_object_or_404(Tag,pk=pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework import generics
from .serializers import RegisterSerializer,MeSerializer
from accounts.models import User

# Generic API views (less code)
class CategoryListCreate(generics.ListCreateAPIView):   # GET list + POST create
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None    # categories are few, no paging


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class MeView(generics.RetrieveAPIView):
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# ViewSet + Router (the main API)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from blog.models import Post
from django.db.models import F,Q,Count
from .serializers import PostSerializer, PostWriteSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = "slug"   # /posts/<slug>/ instead of id

    filterset_fields = ["category", "tags", "author", "status"]
    search_fields = ["title", "body", "author__username"]
    ordering_fields = ["-created_at", "views", "title"]


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
            return qs.filter(Q(status = "published") | Q(author = user))

        return qs.filter(status="published")


    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PostWriteSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

    
