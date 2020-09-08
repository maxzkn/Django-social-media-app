from django import forms
from .models import Post
from users.models import Comment


class PostUploadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "video"]

    # galima pakeisti formą čia (jeigu užkomentuota, tai forma rankiniu būdu padaryta template post_upload.html)
    #     labels = {
    #         "title": "Antraštė",
    #         "video": "Įkelti video",
    #     }

    #     # error_messages = {
    #     #     "title": {"required": "Šis laukas yra privalomas."},
    #     #     "video": {"required": "Šis laukas yra privalomas."},
    #     # }

    # tas pats kas ir error_messages variantas:
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.error_messages = {"required": "Šis laukas yra privalomas."}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["comment"].required = True
    #     self.fields["comment"].error_messages = {
    #         "required": "Laukas negali būti tuščias."
    #     }

    error_messages = {
        "required": "Laukas negali būti tuščias.",
    }

    def clean_comment(self):
        comment = self.cleaned_data.get("comment")
        if comment == "":
            raise forms.ValidationError(
                self.error_messages["required"], code="required"
            )
        return comment


class ChangeTitleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title"]

    # errors:
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["title"].required = True
    #     self.fields["title"].error_messages = {"required": "Pateikite pavadinimą."}

    def clean_title(self):
        new_title = self.cleaned_data.get("title")
        qs = Post.objects.all()
        if qs.filter(title=new_title).exists():
            raise forms.ValidationError("Toks pavadinimas jau egzistuoja.")
        return new_title  # arba bus klaida: this field cannot be null
