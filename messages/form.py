# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from messages.models import Message

class ComposeMailForm(ModelForm):
    class Meta:
        model = Message
        fields = ('message_subject', 'message_text')