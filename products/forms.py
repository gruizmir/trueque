# -*- coding: utf-8 -*-
from django.forms import Form, ModelForm, CharField, EmailField, IntegerField, TextInput, PasswordInput, Textarea, BooleanField,CheckboxInput, FileField, HiddenInput
from django.db import models
from products.models import Product, Category, Comment

class ProductForm(ModelForm):
	product_name = CharField(label='Titulo Producto', widget=TextInput(attrs={'size':40, 'value':'Titulo Producto'}))
	product_description = CharField(label='Descripcion', widget=Textarea(attrs={}))
	product_q_amount = IntegerField(label='Monto', widget=TextInput(attrs={'size':10}))
	class Meta:
		model = Product
		fields = ('product_name', 'product_description', 'product_q_amount')

class CategoryForm(Form):
	field_1 = BooleanField(label=Category.objects.get(id_category=1).category_name, required=False)
	field_2 = BooleanField(label=Category.objects.get(id_category=2).category_name, required=False)
	field_3 = BooleanField(label=Category.objects.get(id_category=3).category_name, required=False)
	field_4 = BooleanField(label=Category.objects.get(id_category=4).category_name, required=False)
	field_5 = BooleanField(label=Category.objects.get(id_category=5).category_name, required=False)
	field_6 = BooleanField(label=Category.objects.get(id_category=6).category_name, required=False)
	field_7 = BooleanField(label=Category.objects.get(id_category=7).category_name, required=False)
	field_8 = BooleanField(label=Category.objects.get(id_category=8).category_name, required=False)
	field_9 = BooleanField(label=Category.objects.get(id_category=9).category_name, required=False)
	field_10 = BooleanField(label=Category.objects.get(id_category=10).category_name, required=False)
	field_11 = BooleanField(label=Category.objects.get(id_category=11).category_name, required=False)
	field_12 = BooleanField(label=Category.objects.get(id_category=12).category_name, required=False)

class ImagesForm(Form):
	img_1 = FileField(label="Imagen 1", max_length=1024)
	img_2 = FileField(label="Imagen 2", max_length=1024)
	img_3 = FileField(label="Imagen 3", max_length=1024)
	img_4 = FileField(label="Imagen 4", max_length=1024)
	img_5 = FileField(label="Imagen 5", max_length=1024)


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('id_comment')

class NewCommentForm(Form):
	comment_subject = CharField(label="Asunto", widget=TextInput(attrs={'size':40}), required=True)
	comment_text = CharField(label="Asunto", widget=Textarea(attrs={}))
