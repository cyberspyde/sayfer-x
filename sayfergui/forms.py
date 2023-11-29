from django.utils.translation import gettext_lazy as _
import json, django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.db import models
from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True)
	saveLogin = forms.BooleanField(required=False)

	class Meta:
		widgets = {
			'username' : forms.TextInput(attrs={'class' : 'form-control'}),
			'password' : forms.TextInput(attrs={'class' : 'form-control'})
			
		}

		labels = {
			'username' : _('username'),
			'password' : _('password'),
			'saveLogin' : _('saveLogin')
		}

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)

class SettingsForm(forms.Form):
	gpt3 = forms.BooleanField(required=False)
	robertaqna = forms.BooleanField(required=False)
	voice_activation = forms.BooleanField(required=False)
	robot_name = forms.CharField(required=True)

	class Meta:
		labels = {
			'gpt3' : _('gpt3'),
			'robertaqna' : _('robertaqna'),
			'voice_activation' : _('voice_activation'),
			'robot_name' : _('robot_name')
		}


	def __init__(self, *args, **kwargs):
		super(SettingsForm, self).__init__(*args, **kwargs)

class EditForm(forms.Form):

	content = forms.CharField( widget=forms.Textarea(attrs={
		'class' : 'form-control'
		}))
	category = forms.CharField( widget=forms.TextInput(attrs={
		'class' : 'form-control'
		}))

	class Meta:
		labels = {
			'content' : _('content'),
			'category' : _('category')
		}
	
	def __init__(self, *args, **kwargs):
		super(EditForm, self).__init__(*args, **kwargs)