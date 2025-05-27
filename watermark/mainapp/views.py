from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings


def add_watermark(image_path, watermark_text):
    # Открываем изображение
    original = Image.open(image_path).convert("RGBA")  # Конвертируем в RGBA

    # Создаем объект для рисования
    txt = Image.new('RGBA', original.size, (255, 255, 255, 0))

    # Настраиваем шрифт и размер
    font_size = int(original.height / 20)  # размер шрифта зависит от высоты изображения
    font = ImageFont.truetype("arial.ttf", font_size)  # Убедитесь, что шрифт доступен
    draw = ImageDraw.Draw(txt)

    # Определяем размер текста и его позицию
    text_width, text_height = draw.textsize(watermark_text, font=font)
    position = (original.width - text_width - 10, original.height - text_height - 10)  # Позиция в правом нижнем углу

    # Накладываем текст на изображение
    draw.text(position, watermark_text, fill=(255, 255, 255, 128), font=font)  # Полупрозрачный белый текст

    # Объединяем оригинальное изображение с текстом
    watermarked = Image.alpha_composite(original, txt)

    # Преобразуем в RGB перед сохранением в JPEG
    watermarked = watermarked.convert("RGB")

    # Сохраняем изображение с водяным знаком
    watermarked_path = os.path.join(settings.MEDIA_ROOT, 'watermarked_' + os.path.basename(image_path))
    watermarked.save(watermarked_path, format='JPEG')  # Сохраняем в формате JPEG

    return watermarked_path

def home(request):
    uploaded_image = None  # для передачи в шаблон
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            # Добавляем водяной знак
            watermarked_image_path = add_watermark(image_instance.image.path, "Ваш Водяной Знак")
            uploaded_image = os.path.basename(watermarked_image_path)  # Получаем имя файла с водяным знаком
            form = ImageUploadForm()  # очистить форму после загрузки
    else:
        form = ImageUploadForm()
    return render(request, 'mainapp/home.html', {'form': form, 'uploaded_image': uploaded_image})