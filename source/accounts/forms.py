from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    avatar = forms.ImageField(required=True, label='Аватар')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'avatar',
            'password1',
            'password2',
            'first_name',
            'bio',
            'phone_number',
            'gender',
        )
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'bio': 'Информация о пользователе',
            'phone_number': 'Номер телефона',
            'gender': 'Пол',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ('first_name', 'bio', 'phone_number', 'gender'):
            self.fields[field_name].required = False
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин или email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
