from django import forms

from .models import *

from django.contrib.auth import get_user_model

from django.contrib.auth.forms import AuthenticationForm

# class PostForm(forms.ModelForm):

#     class Meta:
#         model = Post
#         fields = ('title', 'text',)

# ユーザーモデル取得
User = get_user_model()


class BookshelfForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookshelfForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Bookshelf
        fields = ('title','cat', 'name')
        widgets = {
                    'title': forms.TextInput(attrs={'placeholder':'タイトル（50字まで）',}),
                    'category': forms.Select(),
                    'name': forms.TextInput(attrs={'placeholder':'タイトル（50字まで）','readonly':'readonly'}),
                     }

class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['title'].widget.attrs['readonly'] = 'readonly'
        self.fields['isbn'].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Book
        fields = ('title', 'isbn','comment')
        widgets = {
                    'title': forms.TextInput(),
                    'isbn': forms.TextInput(),
                    'comment': forms.Textarea(attrs={'placeholder':'コメント（100字まで）','cols': 1, 'rows': 5}),
                }

BookFormset = forms.inlineformset_factory(
    Bookshelf, Book, BookForm, fields='__all__',
    extra=0, max_num=10,
)