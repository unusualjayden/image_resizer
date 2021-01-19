from django import forms

from .models import Image


class ImageForm(forms.ModelForm):
    image_from_url = forms.URLField(label='Ссылка', required=False)

    class Meta:
        model = Image
        fields = ['image_file', ]

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image_file'].required = False


class SizeForm(forms.Form):
    width = forms.IntegerField(required=False, label='Ширина')
    height = forms.IntegerField(required=False, label='Высота')
