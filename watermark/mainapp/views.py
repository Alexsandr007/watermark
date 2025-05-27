from django.shortcuts import render, redirect
from .forms import ImageUploadForm

def home(request):
    uploaded_image = None  # для передачи в шаблон
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            uploaded_image = image_instance.image.url  # путь к загруженному файлу
            form = ImageUploadForm()  # очистить форму после загрузки
    else:
        form = ImageUploadForm()
    return render(request, 'mainapp/home.html', {'form': form, 'uploaded_image': uploaded_image})