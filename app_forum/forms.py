from django import forms
from django.contrib.auth.forms import UserCreationForm
from app_forum.models import News, Comments


class MyForm(UserCreationForm):
    """
    Класс - переопределяющий стандартный класс django UserCreationForm.
    Форма регистрации пользователя.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Только буквы, цифры и @/./+/-/_.'
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].help_text = '<ul class="list-reset"><li>Пароль не должен быть похож' \
                                             ' на личную информацию.</li><li>Пароль должен' \
                                             ' содержать не менее 8 символов.</li><li>Пароль не может быть' \
                                             ' часто используемым паролем.</li><li>Пароль не может быть' \
                                             ' полностью числовым.</li></ul>'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].help_text = 'Повторите пароль'
        self.fields['password2'].label = 'Подтверждение пароля'


class NewsForm(forms.ModelForm):
    """
    Класс - форма модели новостей
    """
    class Meta:
        model = News
        fields = ['title', 'description']


class NewsFullForm(NewsForm):
    """
    Дочерний класс, родитель NewsForm - добавляет поле images
    """
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Изображение', required=False
    )

    class Meta(NewsForm.Meta):
        fields = NewsForm.Meta.fields + ['images']


class CommentsForm(forms.ModelForm):
    """
    Класс - форма модели комментариев
    """
    class Meta:
        model = Comments
        fields = 'user_name', 'text_comment'
