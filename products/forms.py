# -*- coding: utf-8 -*-
from django.forms import Form, ModelForm, CharField, EmailField, IntegerField, TextInput, PasswordInput, Textarea, BooleanField,CheckboxInput, FileField, HiddenInput
from django.db import models
from products.models import Product, Category, Comment

#ProductForm:	Formulario para ingresar los datos principales de un nuevo producto.
class ProductForm(ModelForm):
	product_name = CharField(label='Titulo Producto', widget=TextInput(attrs={'size':40, 'placeholder':'Título Producto'}))
	product_description = CharField(label='Descripcion', widget=Textarea(attrs={'size':500, 'placeholder':"Describe tu objeto"}))
	product_q_amount = IntegerField(label='Monto', widget=TextInput(attrs={'size':10, 'placeholder':"000"}))
	class Meta:
		model = Product
		fields = ('product_name', 'product_description', 'product_q_amount')


#CategoryForm:	Formulario para elegir las categorias en que se encuentra un producto. Se usa
#				para busquedas y para ingreso de nuevos productos.
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
	
	
#ImagesForm: Formulario para ingresar las (hasta) cinco imagenes de un nuevo producto.
class ImagesForm(Form):
	img_1 = FileField(label="Imagen 1", max_length=1024)
	img_2 = FileField(label="Imagen 2", max_length=1024)
	img_3 = FileField(label="Imagen 3", max_length=1024)
	img_4 = FileField(label="Imagen 4", max_length=1024)
	img_5 = FileField(label="Imagen 5", max_length=1024)
	


#CommentForm: 	Formulario sin objetivo de ser renderizado, se usa para validar datos al ingresar
#				un nuevo Comentario en un producto.
class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('id_comment')


#NewCommentForm:	Formulario con objeto de ser renderizado. Incluye solo un campo para el Asunto y
#					para el Texto del mensaje. No tiene datos de usuario, dado que este debe estar 
#					logueado para hacer el comentario. Se sacan los datos desde session.
class NewCommentForm(Form):
	comment_subject = CharField(label="Asunto", widget=TextInput(attrs={'size':40}), required=True)
	comment_text = CharField(label="Asunto", widget=Textarea(attrs={}))
