from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from .forms import ImageForm, SizeForm
from .models import Image
from .services import ImageResizer, image_download_handler


class ImageListView(ListView):
    template_name = 'image_list.html'
    model = Image
    context_object_name = 'images'
    queryset = Image.objects.all()


class UploadImageView(CreateView):
    model = Image
    form_class = ImageForm
    template_name = 'upload_image.html'

    def form_valid(self, form):
        if form.files['image_file']:
            self.object = form.save()
        elif form.data['image_from_url']:
            self.object = form.save()
            self.object.image_file = image_download_handler(form.data['image_from_url'], self.object.image_hash)
        self.object = form.save()
        return super(UploadImageView, self).form_valid(form)

    def get_success_url(self):
        return reverse('resizer:edit', kwargs={'image_hash': self.object.image_hash})


class EditImageView(UpdateView):
    queryset = Image.objects.all()
    form_class = SizeForm
    template_name = 'edit_image.html'
    slug_url_kwarg = 'image_hash'
    slug_field = 'image_hash'

    def post(self, request, *args, **kwargs):
        size = (self.request.POST.get('width'), self.request.POST.get('height'))
        image = ImageResizer(self.get_object().image_file.url).resize(size)
        return render(request, self.template_name, context={'image_url': image.get_image_url, 'form': self.form_class})

    def get_context_data(self, **kwargs):
        return {'image_url': self.get_object().image_file.url, 'form': self.form_class()}
