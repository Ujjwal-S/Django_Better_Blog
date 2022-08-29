from django import forms
from .models import Comment, Blog
from django.http import HttpResponseRedirect


class CommentForm(forms.ModelForm):
	# reply_id = forms.CharField(max_length=100)
	class Meta:
		model = Comment
		fields = ['body']
		widgets = {
			'body': forms.TextInput(attrs={'placeholder': 'Add your Comment'})
		}


class BlogCreateForm(forms.ModelForm):
	test_category = forms.CharField(max_length=200)
	class Meta:
		model = Blog
		fields = ['title', 'content', 'status', 'img']


