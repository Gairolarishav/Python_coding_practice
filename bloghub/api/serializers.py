from rest_framework import serializers
from blog.models import Category,Tag,Post,Comment
from accounts.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length = 6)
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def validate_email(self,value):
        if User.objects.filter(email__iexact = value).exists():
            raise serializers.ValidationError("This email is already used.")

        return value

    def create(self,validate_data):
        return User.objects.create_user(**validate_data)  # hashes the password

class MeSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(source= "posts.count", read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "post_count"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ["id", "text", "author", "created_at"]
        read_only_fields = ["id", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # "ali"
    category = CategorySerializer(read_only=True)   # nested object
    tags = TagSerializer(many=True,read_only=True)   # nested list
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()  # custom calculated field
    
    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "body", "image", "author", "category", "tags",
            "status", "views","comment_count", "comments" , "created_at"
        ]

    def get_comment_count(self,obj):  # name must be get_<field>
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