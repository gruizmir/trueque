# -*- coding: utf-8 -*-
from albums.models import Album
from django.forms.models import ModelForm
import albums.utils as albums_utils

ERROR_ALREADYEXIST = "THAT ALBUM ALREADY EXIST, TRY ANOTHER NAME"

#AddAlbumForm: Formulario utilizado para añadir un nuevo album de algun usuario en la db
class AddAlbumForm(ModelForm):
    class Meta:
        model = Album
        exclude = ('id_owner','album_edit')
    def clean(self): 
        cleaned_data = super(AddAlbumForm, self).clean()
        if not albums_utils.add_album(self.id_owner, cleaned_data.get('album_name'), True, True):
            self._errors['album_name'] = self.error_class([ERROR_ALREADYEXIST])
            del cleaned_data['album_name']
        return cleaned_data