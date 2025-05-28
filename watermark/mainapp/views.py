from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings


def add_watermark(image_path, watermark_text, font):
    # Открываем изображение
    original = Image.open(image_path).convert("RGBA")  # Конвертируем в RGBA

    # Создаем объект для рисования
    txt = Image.new('RGBA', original.size, (255, 255, 255, 0))

    # Настраиваем шрифт и размер
    font_size = int(original.height / font)  # размер шрифта зависит от высоты изображения
    font = ImageFont.truetype("arial.ttf", font_size)  # Убедитесь, что шрифт доступен
    draw = ImageDraw.Draw(txt)

    # Определяем размер текста
    text_width, text_height = draw.textsize(watermark_text, font=font)

    # Накладываем текст на изображение в нескольких местах
    y = 0
    while y < original.height:
        x = 0
        while x < original.width:
            # Позиция для каждого водяного знака
            position = (x, y)
            draw.text(position, watermark_text, fill=(255, 255, 255, 128), font=font)  # Полупрозрачный белый текст
            x += text_width + 20  # Переход к следующему водяному знаку по горизонтали
        y += text_height + 20  # Переход к следующему ряду водяных знаков

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
            watermarked_image_path = add_watermark(image_instance.image.path, image_instance.watermark_text, image_instance.font)
            uploaded_image = os.path.basename(watermarked_image_path)  # Получаем имя файла с водяным знаком
            form = ImageUploadForm()  # очистить форму после загрузки
    else:
        form = ImageUploadForm()
    return render(request, 'mainapp/home.html', {'form': form, 'uploaded_image': uploaded_image})