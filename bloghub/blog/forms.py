from django import forms
from .models import Post,Comment

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
        image = self.cleaned_data["image"]
        if image and hasattr(image,"size") and image.size> 2 * 1024 * 1024:
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