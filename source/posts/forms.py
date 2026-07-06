from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'caption')
        labels = {'image': 'Изображение', 'caption': 'Описание'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True
        self.fields['caption'].required = False
        self.fields['caption'].widget = forms.Textarea(attrs={'rows': 3})
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')