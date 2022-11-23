from django import forms
from allauth.account.forms import LoginForm, SignupForm

from .models import Question, MyUser, Comment


class QuestionCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    tags = forms.CharField(max_length=255, label='Теги', required=True)

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']


class UserChangeInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    first_name = forms.CharField(label='Имя', max_length=255, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=255, required=True)
    profile_picture = forms.ImageField(label='Фотография профиля', required=False)

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'profile_picture']


class AddCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = ['content']


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
