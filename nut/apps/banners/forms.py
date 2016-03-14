from django.forms import  ModelForm, TextInput,BooleanField,FileField
from django.forms.fields import ImageField, IntegerField, FloatField

from apps.core.utils.image import  HandleImage


class BaseBannerForm(ModelForm):

    default_banner_fields = ['link', 'applink','position' \
                            ,'status', 'img_file']

    img_file = ImageField(label='upload banner image')

    def __init__(self, *args, **kwargs):
        super(BaseBannerForm, self).__init__(*args, **kwargs)
        for key , field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

    class Meta:
        abstract = True

    def handle_images(self):
        image_field_pair = {'img_file':'image'}
        for form_field_name , model_field_name in image_field_pair.items():
            self.handle_image_field(form_field_name, model_field_name)

    def handle_image_field(self, form_field_name , model_field_name):
        if not self.cleaned_data.get(form_field_name):
            return
        _image_path = self._handle_post_image(form_field_name)
        setattr(self.instance , model_field_name , _image_path )

    def _handle_post_image(self, form_field_name):
        _image = HandleImage(image_file=self.cleaned_data.get(form_field_name))
        _image_path = _image.icon_save()
        return _image_path

    def save(self, commit=True, *args, **kwargs):
        self.handle_images()
        return super(BaseBannerForm,self).save(commit=True, *args, **kwargs)



class BaseBannerCreateForm(BaseBannerForm):
        img_file = ImageField(label='upload banner image' , required=True)

class BaseBannerUpdateForm(BaseBannerForm):
        img_file = ImageField(label='upload banner image' , required=False)



