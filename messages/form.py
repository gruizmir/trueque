# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import ModelForm
from messages.models import Message

class ComposeMailForm(ModelForm):
    user_id = forms.CharField(widget=forms.TextInput(attrs={'style': "display:none;"}))
    class Meta:
        model = Message
        fields = ('subject', 'text')
