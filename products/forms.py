# -*- coding: utf-8 -*-
from django.forms import Form, ModelForm, CharField, EmailField, IntegerField, TextInput, PasswordInput, Textarea, BooleanField,CheckboxInput, FileField, HiddenInput
from django.db import models
from products.models import Product, Category, Comment

#ProductForm:	Formulario para ingresar los datos principales de un nuevo producto.
class ProductForm(ModelForm):
	name = CharField(label=u'Título Producto', widget=TextInput(attrs={'size':40, 'placeholder':'Título Producto'}))
	description = CharField(label=u'Descripción', widget=Textarea(attrs={'size':500, 'placeholder':"Describe tu objeto"}))
	q_amount = IntegerField(label='Monto', widget=TextInput(attrs={'size':10, 'placeholder':"000"}))
	class Meta:
		model = Product
		fields = ('name', 'description', 'q_amount')


#CategoryForm:	Formulario para elegir las categorias en que se encuentra un producto. Se usa
#				para busquedas y para ingreso de nuevos productos.
class CategoryForm(Form):
	field_1 = BooleanField(label=Category.objects.get(id=1).name, required=False)
	field_2 = BooleanField(label=Category.objects.get(id=2).name, required=False)
	field_3 = BooleanField(label=Category.objects.get(id=3).name, required=False)
	field_4 = BooleanField(label=Category.objects.get(id=4).name, required=False)
	field_5 = BooleanField(label=Category.objects.get(id=5).name, required=False)
	field_6 = BooleanField(label=Category.objects.get(id=6).name, required=False)
	field_7 = BooleanField(label=Category.objects.get(id=7).name, required=False)
	field_8 = BooleanField(label=Category.objects.get(id=8).name, required=False)
	field_9 = BooleanField(label=Category.objects.get(id=9).name, required=False)
	field_10 = BooleanField(label=Category.objects.get(id=10).name, required=False)
	field_11 = BooleanField(label=Category.objects.get(id=11).name, required=False)
	field_12 = BooleanField(label=Category.objects.get(id=12).name, required=False)
	
	
#ImagesForm: Formulario para ingresar las (hasta) cinco imagenes de un nuevo producto.
class ImagesForm(Form):
	img_1 = FileField(label="Imagen 1", max_length=1024)
	img_2 = FileField(required=False, label="Imagen 2", max_length=1024)
	img_3 = FileField(required=False, label="Imagen 3", max_length=1024)
	img_4 = FileField(required=False, label="Imagen 4", max_length=1024)
	img_5 = FileField(required=False, label="Imagen 5", max_length=1024)
	


#CommentForm: 	Formulario sin objetivo de ser renderizado, se usa para validar datos al ingresar
#				un nuevo Comentario en un producto.
class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('id')


#NewCommentForm:	Formulario con objeto de ser renderizado. Incluye solo un campo para el Asunto y
#					para el Texto del mensaje. No tiene datos de usuario, dado que este debe estar 
#					logueado para hacer el comentario. Se sacan los datos desde session.
class NewCommentForm(Form):
	subject = CharField(label="Asunto", widget=TextInput(attrs={'size':40}), required=True)
	text = CharField(label="Mensaje", widget=Textarea(attrs={}))
