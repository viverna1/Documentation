from manim import *
import os
from PIL import Image

config.background_color = "#00000000"

class Formula(Scene):
    def construct(self):
        graph = FunctionGraph(lambda x: 2, x_range=[-2,2])
        self.add(graph)
        

if __name__ == "__main__":
    # Рендерим PNG с прозрачным фоном
    os.system("manim -ql render_math.py Formula -s --format=png --transparent")
    
    # Находим последний PNG
    media_dir = "media/images/render_math"
    png_files = [f for f in os.listdir(media_dir) if f.endswith(".png")]
    png_files.sort(key=lambda x: os.path.getmtime(os.path.join(media_dir, x)))
    last_png = os.path.join(media_dir, png_files[-1])
    
    # Обрезка по содержимому с отступом 10 пикселей
    img = Image.open(last_png)
    # Преобразуем в альфа-канал, чтобы понять границы
    alpha = img.split()[-1]
    bbox = alpha.getbbox()  # bbox = (left, upper, right, lower)
    if bbox:
        left, upper, right, lower = bbox
        # Добавляем отступ 10 пикселей, но не выходим за пределы картинки
        left = max(left-10, 0)
        upper = max(upper-10, 0)
        right = min(right+10, img.width)
        lower = min(lower+10, img.height)
        img_cropped = img.crop((left, upper, right, lower))
        img_cropped.save(last_png)

    # Перемещяем PNG в нужную папку
    target_dir = "media/media/math"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    target_path = os.path.join(target_dir, "Formula_ManimCE_v0.19.0.png")
    os.replace(last_png, target_path)
    
    # Удаляем папку videos
    videos_path = "media/videos"
    if os.path.exists(videos_path):
        import shutil
        shutil.rmtree(videos_path)
