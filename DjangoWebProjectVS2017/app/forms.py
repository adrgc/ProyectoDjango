"""
Definition of forms.
"""

from django import forms
from app.models import Question,Choice,User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

categories = set([tuple([x.category,x.category]) for x in Question.objects.all()])

class QuestionForm(forms.ModelForm):

        class Meta:
            model = Question
            fields = ('question_text', 'category',)

class ChoiceForm(forms.ModelForm):

        class Meta:
            model = Choice
            fields = ('choice_text','correct',)

class UserForm(forms.ModelForm):

        class Meta:
            model = User
            fields = ('email','nombre',)

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
class QuestionFilter(forms.Form):
      category = forms.CharField(label='Que categoria quieres buscar', widget=forms.Select(choices=categories))


