from django import forms
from .models import Topic, Post, Board

class NewTopicForm(forms.ModelForm):
	message = forms.CharField(
		widget=forms.Textarea(
			attrs={'rows':5, 'placeholder':'What is in your mind?'}
		), 
		max_length=4000,
		help_text="The max length of the text is 4000."
	)

	class Meta:
		model = Topic
		# subject is a field in Topic model
		# message is a field in Post model
		fields = ['subject', 'message']

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['message']

class NewBoardForm(forms.ModelForm):
	name = forms.CharField(
		max_length=30,
		help_text="name can not be more than 30 words"
	)

	description = forms.CharField(
		max_length=100,
		help_text="max length 100 words"
	)

	class Meta:
		model = Board
		fields = ['name', 'description']

