from django import forms
from .models import Topic


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}),
        max_length=4000,
        help_text='The max length of the text is 4000.')

    class Meta:
        model = Topic

        # Field message refers to message in the Post we want to save
        fields = ['subject', 'message']
