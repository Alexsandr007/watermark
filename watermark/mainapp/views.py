from django.shortcuts import render, redirect
from .forms import ImageUploadForm


def home(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # если используете ModelForm
            # или обработайте файл как угодно
            return redirect('home')
    else:
        form = ImageUploadForm()
    return render(request, 'mainapp/home.html', {'form': form})