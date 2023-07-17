from django import forms

from board.models import Ad, Reply


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ('title', 'content', 'category', )


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('content', )
