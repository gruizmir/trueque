from django.db import models

class Country(models.Model):
    id_country = models.IntegerField(primary_key=True, db_column='ID_country') # Field name made lowercase.
    country_name = models.CharField(max_length=60, db_column='Country_name') # Field name made lowercase.
    class Meta:
        db_table = u'Country'

class City(models.Model):
    id_city = models.IntegerField(primary_key=True, db_column='ID_city') # Field name made lowercase.
    id_country = models.ForeignKey(Country, db_column='ID_country') # Field name made lowercase.
    city_name = models.CharField(max_length=60, db_column='City_name') # Field name made lowercase.
    class Meta:
        db_table = u'City'

class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True, db_column='ID_usuario') # Field name made lowercase.
    usuario_password = models.CharField(max_length=75, db_column='Usuario_password') # Field name made lowercase.
    usuario_name = models.CharField(max_length=60, db_column='Usuario_name') # Field name made lowercase.
    usuario_lastname = models.CharField(max_length=60, db_column='Usuario_lastname') # Field name made lowercase.
    usuario_bullletins = models.IntegerField(db_column='Usuario_bullletins') # Field name made lowercase.
    usuario_email_1 = models.CharField(max_length=90, db_column='Usuario_email_1') # Field name made lowercase.
    usuario_email_2 = models.CharField(max_length=90, db_column='Usuario_email_2', blank=True) # Field name made lowercase.
    usuario_phone_1 = models.CharField(max_length=30, db_column='Usuario_phone_1', blank=True) # Field name made lowercase.
    usuario_phone_2 = models.CharField(max_length=30, db_column='Usuario_phone_2', blank=True) # Field name made lowercase.
    usuario_language = models.CharField(max_length=15, db_column='Usuario_language', blank=True) # Field name made lowercase.
    usuario_fb_token = models.CharField(max_length=450, db_column='Usuario_FB_Token', blank=True) # Field name made lowercase.
    usuario_tw_token = models.CharField(max_length=480, db_column='Usuario_TW_Token', blank=True) # Field name made lowercase.
    usuario_register_date = models.DateTimeField(db_column='Usuario_register_date') # Field name made lowercase.
    usuario_city = models.ForeignKey(City, null=True, db_column='Usuario_city', blank=True) # Field name made lowercase.
    usuario_level = models.IntegerField(db_column='Usuario_level') # Field name made lowercase.
    usuario_rating = models.IntegerField(db_column='Usuario_rating') # Field name made lowercase.
    usuario_ranking_qty = models.IntegerField(null=True, db_column='Usuario_ranking_qty', blank=True) # Field name made lowercase.
    usuario_quds = models.IntegerField(db_column='Usuario_quds') # Field name made lowercase.
    usuario_follower_qty = models.IntegerField(db_column='Usuario_follower_qty') # Field name made lowercase.
    usuario_followe_qty = models.IntegerField(db_column='Usuario_followe_qty') # Field name made lowercase.
    usuario_barter_qty = models.IntegerField(db_column='Usuario_barter_qty') # Field name made lowercase.
    usuario_remaining_invitations = models.IntegerField(db_column='Usuario_remaining_invitations') # Field name made lowercase.
    usuario_art = models.IntegerField(db_column='Usuario_art') # Field name made lowercase.
    usuario_music = models.IntegerField(db_column='Usuario_music') # Field name made lowercase.
    usuario_tech = models.IntegerField(db_column='Usuario_tech') # Field name made lowercase.
    usuario_cars = models.IntegerField(db_column='Usuario_cars') # Field name made lowercase.
    usuario_travels = models.IntegerField(db_column='Usuario_travels') # Field name made lowercase.
    usuario_clothes = models.IntegerField(db_column='Usuario_clothes') # Field name made lowercase.
    usuario_cine = models.IntegerField(db_column='Usuario_cine') # Field name made lowercase.
    use_sports = models.IntegerField(db_column='Use_sports') # Field name made lowercase.
    usuario_eco = models.IntegerField(db_column='Usuario_eco') # Field name made lowercase.
    usuario_culture = models.IntegerField(db_column='Usuario_culture') # Field name made lowercase.
    usuario_spectacles = models.IntegerField(db_column='Usuario_spectacles') # Field name made lowercase.
    usuario_love = models.IntegerField(db_column='Usuario_love') # Field name made lowercase.
    usuario_food = models.IntegerField(db_column='Usuario_food') # Field name made lowercase.
    usuario_vacations = models.IntegerField(db_column='Usuario_vacations') # Field name made lowercase.
    usuario_services = models.IntegerField(db_column='Usuario_services') # Field name made lowercase.
    class Meta:
        db_table = u'Usuario'

class Warningreason(models.Model):
    id_reason = models.IntegerField(primary_key=True, db_column='ID_reason') # Field name made lowercase.
    reason_text = models.CharField(max_length=150, db_column='Reason_text') # Field name made lowercase.
    class Meta:
        db_table = u'WarningReason'

class Warnings(models.Model):
    id_warning = models.IntegerField(primary_key=True, db_column='ID_warning') # Field name made lowercase.
    id_sender = models.ForeignKey(Usuario, db_column='ID_sender') # Field name made lowercase.
    id_receiver = models.ForeignKey(Usuario, db_column='ID_receiver', related_name="+") # Field name made lowercase.
    warning_reason = models.ForeignKey(Warningreason, null=True, db_column='Warning_reason', blank=True) # Field name made lowercase.
    warning_message = models.TextField(db_column='Warning_message') # Field name made lowercase.
    warning_datetime = models.IntegerField(db_column='Warning_datetime') # Field name made lowercase.
    class Meta:
        db_table = u'Warning'

class Rating(models.Model):
    id_rating = models.IntegerField(primary_key=True, db_column='ID_rating') # Field name made lowercase.
    id_rater = models.ForeignKey(Usuario, null=True, db_column='ID_rater', blank=True, related_name="+") # Field name made lowercase.
    id_rated = models.ForeignKey(Usuario, db_column='ID_rated') # Field name made lowercase.
    rating_level = models.IntegerField(db_column='Rating_level') # Field name made lowercase.
    rating_datetime = models.DateTimeField(db_column='Rating_datetime') # Field name made lowercase.
    class Meta:
        db_table = u'Rating'

class Followers(models.Model):
    id_follower = models.ForeignKey(Usuario, primary_key=True, db_column='ID_follower') # Field name made lowercase.
    id_followed = models.ForeignKey(Usuario, db_column='ID_followed', related_name="+") # Field name made lowercase.
    class Meta:
        db_table = u'Followers'
